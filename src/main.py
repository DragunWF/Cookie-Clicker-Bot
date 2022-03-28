import asyncio
import json
import os
from pathlib import Path
from colored import fg

from bot import Bot
from controller import BotController
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
    root_dir = os.path.dirname(os.path.abspath(__file__))
    while "\\" in root_dir:
        root_dir = root_dir.replace("\\", "/")

    settings = json.loads(Path("data/settings.json").read_text())[0]
    settings["save_file_location"] = f"{root_dir}/{settings['saves']['location']}"

    session = Session()
    Utils.tts_print("Session has been created!", color="green")

    if settings["controlled"]:
        bot = BotController(session, settings)
        asyncio.run(bot.input_loop())
    else:
        bot = Bot(session, settings)
        asyncio.run(bot.run())


if __name__ == "__main__":
    main()
