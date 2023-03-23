import random
import huepy
from instabot import Bot


class InstagramBot(Bot):
    def __init__(self, max_follows_per_day, max_unfollows_per_day):
        super().__init__()
        self.delays["follow"] = random.randint(200, 300)
        self.max_per_day["follows"] = max_follows_per_day
        self.max_per_day["unfollows"] = max_unfollows_per_day
        self.save_logfile = False

    def console_print(self, text, color=None):
        if self.verbosity:
            text = text
            if color is not None:
                text = getattr(huepy, "grey")(text)
            print(text)