import json
import os
from pathlib import Path
from colored import fg

from bot import Bot
from session import Session
from utils import Utils


def user_choose(question: str) -> bool:
    while True:
        option = input(fg("light_green") +
                       f"{question} (y/n) ").strip().lower()
        if option == "y" or option == "yes":
            return True
        if option == "n" or option == "no":
            return False
        Utils.colored_print("Invalid option!", color="red")


def configuration():
    pass


def main():
    root_directory = os.path.dirname(os.path.abspath(__file__))
    settings = json.loads(Path("data/settings.json").read_text())[0]

    session = Session()
    bot = Bot(session, settings)
    Utils.tts_print("Bot is now running!", color="green")
    bot.run()


if __name__ == "__main__":
    main()
