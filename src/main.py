import asyncio
import json
import os
from pathlib import Path
from colored import fg

from bot import Bot
from controller import BotController
from session import Session
from utils import Utils

green, yellow, cyan, white = fg("light_green"), fg(
    "light_yellow"), fg("light_cyan"), fg("white")


def user_choose(question: str) -> bool:
    while True:
        option = input(green + f"{question} (y/n) " + white).strip().lower()
        if option == "y" or option == "yes":
            return True
        if option == "n" or option == "no":
            return False
        Utils.colored_print("Invalid option!", color="red")


def configuration(settings: dict) -> dict:
    Utils.colored_print("Warning: Invalid configuration will result in an error!", color="red")
    settings["controlled"] = user_choose("Do you want the bot's automation to be controlled?")

    if settings["controlled"]:
        default_controls = user_choose("Do you want to use the default controls?")
        if not default_controls:
            start_key = input(green + "Key for starting automation" + white).strip().lower()
            stop_key = input(yellow + "Key for stopping automation" + white).strip().lower()
            quit_key = input(cyan + "Key for quitting/turning off the bot" + white).strip().lower()
            settings["controls"]["start_automation"] = start_key
            settings["controls"]["stop_automation"] = stop_key
            settings["controls"]["quit_game"] = quit_key
            
    load_save = user_choose("Do you want to load a save file?")
    if load_save:
        Utils.colored_print("Specify a valid save file path from this project's main root directory",
                            color="yellow")
        settings["saves"]["load_save_file"] = True
        settings["saves"]["location"] = input(cyan + "Save file path: " + white).strip()
    else:
        settings["saves"]["load_save_file"] = False

        randomized_name = user_choose("Do you want to have a randomized bakery name?")
        if randomized_name:
            bakery_name = input(yellow + "Your bakery name: " + white).strip()
            settings["bakery_names"] = [bakery_name]

    return settings


def main():
    settings = json.loads(Path("data/settings.json").read_text())[0]
    default = user_choose("Do you want to use the default settings?")

    if not default:
        settings = configuration(settings)

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    while "\\" in root:
        root = root.replace("\\", "/")
    root = "".join([i if i != ":" else f"{i}/" for i in root])
    root = f"{root[0].upper()}{root[1:]}"
    settings["save_file_location"] = f"{root}/{settings['saves']['location']}"

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
