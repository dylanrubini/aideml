from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model

MAP_TOKENS = 4096
MAX_CHAT_HISTORY_TOKENS = 8 * MAP_TOKENS
MAX_REFLECTIONS = 5


class AiderAgent:

    def __init__(self, model_type, chat_history_file, temperature):

        self.model_type = model_type
        self.chat_history_file = chat_history_file
        self.temperature = temperature

        self.io = InputOutput(
            yes=True,  # Say yes to every suggestion aider makes
            chat_history_file=self.chat_history_file,  # Log the chat here
            input_history_file="/dev/null",  # Don't log the "user input"
        )

        self.model = Model(self.model_type)

        self.coder = Coder.create(
            main_model=self.model,
            io=self.io,
            # git_dname=git_dname,  # TODO: what is this
            map_tokens=MAP_TOKENS,  # MAP_TOKENS for the repo map
            stream=False,
            auto_commits=False,  # Don't bother git committing changes
            # fnames=oracle_files,  # TODO: these are files we want aider to work on
            auto_test=False,  # not testing automatically
            test_cmd=None,
            # max_chat_history_tokens=MAX_CHAT_HISTORY_TOKENS,  # TODO
            edit_format="diff",
            # verbose=True,
        )

        self.coder.temperature = self.temperature

        # Take at most 4 steps before giving up.
        # Usually set to 5, but this reduces API costs.
        self.coder.max_reflections = MAX_REFLECTIONS

        # Add announcement lines to the markdown chat log
        self.coder.show_announcements()

    def run(self):

        return coder.run()
