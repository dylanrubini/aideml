import re
from pathlib import Path

from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model
from aider.repo import GitRepo

from .openai_api_pricing import OAI_Pricing
from .utils import compile_prompt_to_md

MAP_TOKENS = 4096
MAX_CHAT_HISTORY_TOKENS = 8 * MAP_TOKENS
MAX_REFLECTIONS = 5


class AiderAgent:

    def __init__(
        self,
        model_type: str,
        chat_history_file: Path,
        repo_dir: Path,
        temperature: float,
        per_run_token_limit: int,
    ):

        self.model_type = model_type
        self.chat_history_file = chat_history_file
        self.repo_dir = repo_dir
        self.temperature = temperature
        self.per_run_token_limit = per_run_token_limit

        self.chat_history_file = self.chat_history_file.joinpath("history.log")
        self.oai_spending = OAI_Pricing(
            self.model_type, self.per_run_token_limit
        )

        self.io = InputOutput(
            yes=True,  # Say yes to every suggestion aider makes
            chat_history_file=self.chat_history_file,  # Log the chat here
            input_history_file="/dev/null",  # Don't log the "user input"
        )

        self.model = Model(self.model_type)
        self.model.max_chat_history_tokens = MAX_CHAT_HISTORY_TOKENS

        fnames = ["run_simulation.py"]
        fnames = [
            self.repo_dir.joinpath("examples/scripts").joinpath(f)
            for f in fnames
        ]
        # fnames = None

        self.git_repo = GitRepo(
            io=self.io, fnames=fnames, git_dname=self.repo_dir.resolve()
        )

        self.coder = Coder.create(
            main_model=self.model,
            io=self.io,
            repo=self.git_repo,
            map_tokens=MAP_TOKENS,  # No. tokens to create repo map
            stream=False,
            auto_commits=False,  # No git committing
            fnames=fnames,  # TODO: these are files we want aider to work on
            auto_test=False,  # not testing automatically
            test_cmd=None,
            edit_format="diff",
            # verbose=True,
            detect_urls=False,  # prevent it scarping from the web, FOR NOW
        )

        self.coder.temperature = self.temperature
        self.coder.max_reflections = MAX_REFLECTIONS
        self.coder.show_announcements()

    def run(self, prompt: str) -> str:

        # TODO: currently disabled "preproc" flag because it caused all files
        # in repo to be added to context and overloaded it
        output_code = self.coder.run(
            compile_prompt_to_md(prompt), preproc=False
        )

        n_tokens = self.extract_tokens()
        self.oai_spending.update(n_tokens // 2, n_tokens // 2)
        self.oai_spending.print()

        return output_code

    def extract_tokens(self):

        # Read the last line
        with self.chat_history_file.open("rb") as fh:
            fh.seek(-2, 2)  # Move the pointer to EOF
            while (
                fh.read(1) != b"\n"
            ):  # Move backwards until the last newline is found
                fh.seek(-2, 1)
            last_line = (
                fh.readline().decode().strip()
            )  # Read the last line and decode

        if not last_line.startswith("> Tokens:"):
            raise RuntimeError("AIDER has not displayed number of tokens")

        n_tokens = (
            self.extract_first_int(last_line) * 1000
        )  # because output is in units of "k" tokens
        return n_tokens

    def extract_first_int(self, s):
        match = re.search(r"\d+", s)  # Finds the first sequence of digits
        return int(match.group()) if match else None  # Convert to int if found
