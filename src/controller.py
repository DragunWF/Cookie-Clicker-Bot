import asyncio
import keyboard

from bot import Bot
from utils import Utils


class BotController(Bot):
    def __init__(self):
        self.automation_running = True
        Utils.tts_print("Bot Controller has been initialized!", color="green")

    async def input_loop(self):
        while True:
            if keyboard.is_pressed("num 1"):
                if not self.automation_running:
                    self.automation_running = True
                    Utils.tts_print("Automation on", color="green")
                else:
                    Utils.colored_print("Automation is already on", color="red")
            elif keyboard.is_pressed("num 2"):
                if self.automation_running:
                    self.automation_running = False
                    Utils.tts_print("Automation off", color="yellow")
                else:
                    Utils.colored_print("Automation is already off", color="red")

            if self.automation_running:
                asyncio.run(self.run())
