import copy
import logging
import random
from typing import Any, Callable, cast

import humanize

from .backend import FunctionSpec, aider_agent, query
from .interpreter import ExecutionResult
from .journal import Journal, Node
from .utils import data_preview
from .utils.config import Config
from .utils.metric import MetricValue, WorstMetricValue
from .utils.response import extract_code, extract_text_up_to_code, wrap_code

logger = logging.getLogger("aide")


ExecCallbackType = Callable[[str, bool], ExecutionResult]

review_func_spec = FunctionSpec(
    name="submit_review",
    json_schema={
        "type": "object",
        "properties": {
            "is_bug": {
                "type": "boolean",
                "description": "true if the output log shows that the execution failed or has some bug, otherwise false.",
            },
            "summary": {
                "type": "string",
                "description": "if there is a bug, propose a fix. Otherwise, write a short summary (2-3 sentences) describing the empirical findings.",
            },
            "metric": {
                "type": "number",
                "description": "If the code ran successfully, report the value of the validation metric. Otherwise, leave it null.",
            },
            "lower_is_better": {
                "type": "boolean",
                "description": "true if the metric should be minimized (i.e. a lower metric value is better, such as with MSE), false if the metric should be maximized (i.e. a higher metric value is better, such as with accuracy).",
            },
        },
        "required": ["is_bug", "summary", "metric", "lower_is_better"],
    },
    description="Submit a review evaluating the output of the training script.",
)


class Agent:
    def __init__(
        self,
        task_desc: str,
        paper_content: str,
        cfg: Config,
        journal: Journal,
    ):
        super().__init__()
        self.task_desc = task_desc
        self.paper_content = paper_content
        self.cfg = cfg
        self.acfg = cfg.agent
        self.journal = journal
        self.data_preview: str | None = None

        self.aider_agent = aider_agent.AiderAgent(
            model_type=self.acfg.code.model,
            chat_history_file=self.cfg.aider_history_dir,
            repo_dir=cfg.workspace_dir.joinpath("repo/"),
            temperature=self.acfg.code.temp,
            per_run_token_limit=self.acfg.search.per_run_token_limit,
        )

    def search_policy(self) -> Node | None:
        """Select a node to work on (or None to draft a new node)."""
        search_cfg = self.acfg.search

        # initial drafting
        if len(self.journal.draft_nodes) < search_cfg.num_drafts:
            logger.debug(
                "[search policy] drafting new node (not enough drafts)"
            )
            return None

        # debugging
        if random.random() < search_cfg.debug_prob:
            # nodes that are buggy + leaf nodes + debug depth < max debug depth
            debuggable_nodes = [
                n
                for n in self.journal.buggy_nodes
                if (n.is_leaf and n.debug_depth <= search_cfg.max_debug_depth)
            ]
            if debuggable_nodes:
                logger.debug("[search policy] debugging")
                return random.choice(debuggable_nodes)
            logger.debug("[search policy] not debugging by chance")

        # back to drafting if no nodes to improve
        good_nodes = self.journal.good_nodes
        if not good_nodes:
            logger.debug("[search policy] drafting new node (no good nodes)")
            return None

        # greedy
        greedy_node = self.journal.get_best_node()
        logger.debug("[search policy] greedy node selected")
        return greedy_node

    @property
    def _prompt_environment(self):
        pkgs = [
            "pybamm",
            "casadi",
            "scipy",
            "numpy",
            "matplotlib",
        ]  # TODO: generalize
        random.shuffle(pkgs)
        pkg_str = ", ".join([f"`{p}`" for p in pkgs])

        env_prompt = {
            "Installed Packages": f"Your solution can use any relevant packages such as: {pkg_str}."
        }
        return env_prompt

    @property
    def _prompt_impl_guideline(self):
        impl_guideline = [
            "The code should **implement the proposed solution**",
            "The code should be a single-file python program that is self-contained and can be executed as-is.",
            "No parts of the code should be skipped, don't terminate the before finishing the script.",
            "Your response should only contain a single code block.",
            f"Be aware of the running time of the code, it should complete within {humanize.naturaldelta(self.cfg.exec.timeout)}.",
            "**Please save the requested figure as figure.png**. if the figure has multiple parts, ensure to combine in subplots."
            'Create a submission.json file with the data contained within the figure and store in the "./working" directory. This is extremely important since this file is used for grading/evaluation. DO NOT FORGET THE submission.json file!',
            'You can also use the "./working" directory to store any temporary files that your code needs to create. or figures of datafiles',
        ]
        if self.acfg.expose_prediction:
            impl_guideline.append(
                "The implementation should include a predict() function, "
                "allowing users to seamlessly reuse the code to make predictions on new data. "
                "The prediction function should be well-documented, especially the function signature."
            )

        if self.acfg.k_fold_validation > 1:
            impl_guideline.append(
                f"The evaluation should be based on {self.acfg.k_fold_validation}-fold cross-validation but only if that's an appropriate evaluation for the task at hand."
            )

        return {"Implementation guideline": impl_guideline}

    @property
    def _prompt_resp_fmt(self):
        return {
            "Response format": (
                "Your response should be a brief outline/sketch of your proposed solution in natural language (3-10 sentences), "
                "followed by a single markdown code block (wrapped in ```) which implements this solution, plots and saves the Figure, and stores the Figure data in the submission.json file"
                "There should be no additional headings or text in your response. Just natural language text followed by a newline and then the markdown code block. "
            )
        }

    def do_plan(self, prompt) -> str:

        prompt_plan = copy.copy(prompt)

        prompt_plan["Instructions"] |= {
            "Response format": (
                "Your response should firstly be a detailed outline of your proposed solution in natural language without code yet describing each step of the code implementation."
                "There should be no additional headings or text in your response. Just natural language text"
            )
        }

        return query(
            system_message=prompt_plan,
            user_message=None,
            model=self.acfg.code.model,
            temperature=self.acfg.code.temp,
            per_run_token_limit=self.acfg.search.per_run_token_limit,
        )

    def do_code(self, plan, prompt) -> str:

        prompt_code = copy.copy(prompt)

        prompt_code["Plan"] = plan
        prompt_code["Instructions"] |= self._prompt_impl_guideline

        output_code = extract_code(self.aider_agent.run(prompt_code))

        if not output_code:
            raise RuntimeError("Not code produced by AIDER AI Coder")

        return output_code

    def plan_and_code_query(self, prompt) -> tuple[str, str]:
        """Generate a natural language plan + code in the same LLM call and split them apart."""

        # Include journal publication as context
        prompt["Article"] = self.paper_content

        plan = self.do_plan(prompt)
        code = self.do_code(plan, prompt)

        return plan, code

    def _draft(self) -> Node:
        prompt: Any = {
            "Introduction": (
                "You are a leading expert in computational science and engineering with the goal of writing + running code to reproduce a single or set of figures in a academic publication released very recently. "
                "In order to accurately reproduce the figure, you need to come up with an excellent and creative plan "
                "for a solution and then implement this solution in Python by leveraging a library explained the task description. "
                "We will now provide a description of the task."
            ),
            "Task description": self.task_desc,
            "Memory": self.journal.generate_summary(),
            "Instructions": {},
        }
        prompt["Instructions"] |= {
            "Solution sketch guideline": [
                "This first solution design should be relatively simple. Coding enhancements can be introduced through iterative improvements",
                "Take the Memory section into consideration when proposing the design,"
                "The solution sketch should be 3-10 sentences.",
                "Don't suggest to do EDA.",
            ],
        }
        prompt["Instructions"] |= self._prompt_environment

        if self.acfg.data_preview:
            prompt["Data Overview"] = self.data_preview

        plan, code = self.plan_and_code_query(prompt)
        return Node(plan=plan, code=code)

    def _improve(self, parent_node: Node) -> Node:
        prompt: Any = {
            "Introduction": (
                "You are a leading expert in computational science and engineering attempting to reproduce results in an academic paper."
                " You are provided with a previously developed"
                "solution below and should improve it in order to ensure the results are correct and reproduce the figure in the paper requested in the task description"
                "For this you should first outline a brief plan in natural language for how the solution can be improved and "
                "then implement this improvement in Python based on the provided previous solution. "
            ),
            "Task description": self.task_desc,
            "Memory": self.journal.generate_summary(),
            "Instructions": {},
        }
        prompt["Previous solution"] = {
            "Code": wrap_code(parent_node.code),
        }

        prompt["Instructions"] |= {
            "Solution improvement sketch guideline": [
                "The solution sketch should be a brief natural language description of how the previous solution can be improved.",
                "You should be very specific and should only propose a single actionable improvement.",
                "This improvement should be atomic so that we can experimentally evaluate the effect of the proposed change.",
                "Take the Memory section into consideration when proposing the improvement.",
                "The solution sketch should be 3-10 sentences.",
                "Don't suggest to do EDA.",
            ],
        }

        plan, code = self.plan_and_code_query(prompt)
        return Node(
            plan=plan,
            code=code,
            parent=parent_node,
        )

    def _debug(self, parent_node: Node) -> Node:
        prompt: Any = {
            "Introduction": (
                "You are a leading expert in computational science and engineering attempting to reproduce results in an academic paper. "
                "Your previous solution had a bug, so based on the information below, you should revise it in order to fix this bug. "
                "Your response should be an implementation outline in natural language,"
                " followed by a single markdown code block which implements the bugfix/solution."
            ),
            "Task description": self.task_desc,
            "Previous (buggy) implementation": wrap_code(parent_node.code),
            "Execution output": wrap_code(parent_node.term_out, lang=""),
            "Instructions": {},
        }
        prompt["Instructions"] |= {
            "Bugfix improvement sketch guideline": [
                "You should write a brief natural language description (3-10 sentences) of how the issue in the previous implementation can be fixed.",
                "Don't suggest to do EDA.",
            ],
        }

        if self.acfg.data_preview:
            prompt["Data Overview"] = self.data_preview

        plan, code = self.plan_and_code_query(prompt)
        return Node(plan=plan, code=code, parent=parent_node)

    def _critic(self, parent_node: Node) -> Node:
        prompt: Any = {
            "Introduction": (
                "You are a leading expert in computational science and engineering attempting to reproduce results in an academic paper. "
                "Your role is to determine whether the code previously implemented follows the same implementation described in the Article markdown file"
                "Your response should be an implementation outline in natural language. "
                "If the implementation discussed in the Article and the code implemented are not consistent, create a plan to fix it "
                " followed by a single markdown code block which implements a solution that is faithful with implementation described in the paper."
            ),
            "Task description": self.task_desc,
            "Current implementation": wrap_code(parent_node.code),
            "Execution output": wrap_code(parent_node.term_out, lang=""),
            "Instructions": {},
        }
        prompt["Instructions"] |= {
            "Faithfulness improvement sketch guideline": [
                "You should write a brief natural language plan (3-10 sentences) of how the issue in the previous implementation can be fixed.",
                "Don't suggest to do EDA.",
            ],
        }

        if self.acfg.data_preview:
            prompt["Data Overview"] = self.data_preview

        plan, code = self.plan_and_code_query(prompt)
        return Node(plan=plan, code=code, parent=parent_node)

    def update_data_preview(
        self,
    ):
        self.data_preview = data_preview.generate(self.cfg.workspace_dir)

    def step(self, exec_callback: ExecCallbackType):
        if not self.journal.nodes or self.data_preview is None:
            self.update_data_preview()

        parent_node = self.search_policy()
        logger.debug(
            f"Agent is generating code, parent node type: {type(parent_node)}"
        )

        if parent_node is None:
            print("Drafting...")
            result_node = self._draft()
            print("done!")
        elif parent_node.is_buggy:
            print("Debugging...")
            result_node = self._debug(parent_node)
            print("done!")
        else:
            print("Improving...")
            result_node = self._improve(parent_node)
            print("done!")

        self.parse_exec_result(
            node=result_node,
            exec_result=exec_callback(result_node.code, True),
        )
        self.journal.append(result_node)

    def parse_exec_result(self, node: Node, exec_result: ExecutionResult):
        print("Agent is parsing execution results for node {node.id}")
        logger.info(f"Agent is parsing execution results for node {node.id}")

        node.absorb_exec_result(exec_result)

        prompt = {
            "Introduction": (
                "You are a leading expert in computational science and engineering attempting to reproduce results in an academic paper. "
                "You have written code to solve this task and now need to evaluate the output of the code execution. "
                "You should determine if there were any bugs as well as report the empirical findings."
                "By looking at the Figure data within the file submission.json in the directory './working', you should rate the output from 0.0 to 1.0, where the best result is 1.0."
                "This rating should be based on the physicality of the results and whether they make sense or not. "
                "The judgement should be analogous to a expert Professor looking at the results and judging based on experience whether they are likely to be accurate or not."
            ),
            "Task description": self.task_desc,
            "Implementation": wrap_code(node.code),
            "Execution output": wrap_code(node.term_out, lang=""),
            "submission.json results": wrap_code(
                node.submission_results, lang=""
            ),
        }

        response = cast(
            dict,
            query(
                system_message=prompt,
                user_message=None,
                func_spec=review_func_spec,
                model=self.acfg.feedback.model,
                temperature=self.acfg.feedback.temp,
                per_run_token_limit=self.acfg.search.per_run_token_limit,
            ),
        )

        # if the metric isn't a float then fill the metric with the worst metric
        if not isinstance(response["metric"], float):
            response["metric"] = None

        node.analysis = response["summary"]
        node.is_buggy = (
            response["is_bug"]
            or node.exc_type is not None
            or response["metric"] is None
        )

        if node.is_buggy:
            node.metric = WorstMetricValue()
        else:
            node.metric = MetricValue(
                response["metric"], maximize=not response["lower_is_better"]
            )
