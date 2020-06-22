
from dataclasses import dataclass
from typing import List


@dataclass
class Message():
    text: str
    style: str = 'normal'
    fg: int = 0
    bg: int = 0


class Logger:
    """An object that can log messages."""

    def __init__(self, log_limit: int = 5):

        # the max amount of messages to display
        self.log_limit = log_limit

        # contains all the logged messages
        self.log_messages: List[Message] = []

    def get_log(self) -> List[Message]:
        return self.log_messages

    def log(self, text: str, fg=15, bg=0, style='normal'):
        """Log a message."""

        lines = text.splitlines()

        for line in lines:

            # insert to the front of the list
            self.log_messages.insert(0, Message(line, style, fg, bg))
            # self.log_messages.append(Message(text, style, fg, bg))

            # delete last message if above log_limit
            if len(self.log_messages) > self.log_limit:
                del self.log_messages[self.log_limit]
                # del self.log_messages[0]

    def info(self, text: str):
        self.log(text, 8)  # dark gray
