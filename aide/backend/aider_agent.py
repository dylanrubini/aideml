from pathlib import Path

from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model
from aider.repo import GitRepo

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
    ):

        self.model_type = model_type
        self.chat_history_file = chat_history_file
        self.repo_dir = repo_dir
        self.temperature = temperature

        self.io = InputOutput(
            yes=True,  # Say yes to every suggestion aider makes
            chat_history_file=self.chat_history_file.joinpath(
                "history.log"
            ),  # Log the chat here
            input_history_file="/dev/null",  # Don't log the "user input"
        )

        self.model = Model(self.model_type)
        self.model.max_chat_history_tokens = MAX_CHAT_HISTORY_TOKENS

        # fnames = ["run_simulation.py"]
        # fnames = [self.repo_dir.joinpath(
        #     "examples/scripts").joinpath(f) for f in fnames]
        fnames = None

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

        # TODO: currently disabled preproc because it caused all files
        # in repo to be added to context and overloaded it
        return self.coder.run(compile_prompt_to_md(prompt), preproc=False)
