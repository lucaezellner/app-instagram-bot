import random
import huepy
from instabot import Bot


class InstagramBot(Bot):
    def __init__(self):
        super().__init__()
        self.delays["follow"] = random.randint(200, 400)
        self.max_follows_per_day = 200
        self.max_unfollows_per_day = 200
        # self.logger.setLevel("ERROR")
        # self.api.logger.setLevel("ERROR")

    def console_print(self, text, color=None):
        if self.verbosity:
            text = text
            if color is not None:
                text = getattr(huepy, "grey")(text)
            print(text)
