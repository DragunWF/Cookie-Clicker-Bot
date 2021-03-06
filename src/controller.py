import asyncio
import keyboard
from sys import exit

from bot import Bot
from utils import Utils


class BotController(Bot):
    def __init__(self, session: object, settings: dict):
        super().__init__(session, settings)
        self.__automation_running = True
        self.__controls = settings["controls"]

        Utils.tts_print("Bot Controller has been initialized!", color="green")
        asyncio.run(self.run())

    async def input_loop(self):
        while True:
            if keyboard.is_pressed(self.__controls["start_automation"]):
                if not self.__automation_running:
                    self.__automation_running = True
                    Utils.tts_print("Automation on", color="green")
                else:
                    Utils.tts_print("Automation is already on", color="red")
            elif keyboard.is_pressed(self.__controls["stop_automation"]):
                if self.__automation_running:
                    self.__automation_running = False
                    Utils.tts_print("Automation off", color="yellow")
                else:
                    Utils.tts_print("Automation is already off", color="red")
            elif keyboard.is_pressed(self.__controls["quit_game"]):
                Utils.tts_print("Stopping automation", color="yellow")
                self.__automation_running = False
                self.grab_stats(True)
                self.save_game()
                self.__session.save_session()
                Utils.tts_print("Game has been saved!", color="green")
                Utils.tts_print("Quitting Game", color="cyan")
                exit()

            if self.__automation_running:
                await self.actions()
