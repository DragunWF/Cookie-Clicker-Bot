import asyncio
import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from utils import Utils


class Bot:
    def __init__(self, session, settings):
        self.controlled = settings["controlled"]
        self.bakery_names = tuple(settings["bakery_names"])
        self.session = session

        if settings["saves"]["load_save_file"]:
            self.save_file_location = settings["save_file_location"]

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get("https://orteil.dashnet.org/cookieclicker/")
        self.driver.maximize_window()

        self.cookie = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "bigCookie"))
        )
        self.cookie_count = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "cookies"))
        )
        self.products = None
        self.iteration = 0

        Utils.tts_print("Bot has been initialized", color="green")
        sleep(1)

    def grab_stats(self, session_ending):
        stats_button = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "statsButton"))
        )
        stats_button.click()

        stats = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "subsection"))
        )
        self.session.save_session_stats(stats.text.split("\n"), session_ending)

        stats_button.click()

    def save_game(self):
        pass

    def load_save_file(self):
        options_button = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "prefsButton"))
        )
        options_button.click()

        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "FileLoadInput"))
        ).send_keys(self.save_file_location)

        options_button.click()

    def change_bakery_name(self):
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "bakeryName"))
        ).click()
        name_input = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "bakeryNameInput"))
        )
        name_input.clear()
        name_input.send_keys(random.choice(self.bakery_names))
        self.driver.find_element_by_id("promptOption0").click()

    def close_pop_ups(self):
        self.pop_ups = tuple(self.driver.find_elements_by_class_name("close"))
        for pop_up in self.pop_ups:
            try:
                pop_up.click()
            except:
                continue

    def check_golden_cookies(self):
        shimmers = tuple(self.driver.find_elements_by_class_name("shimmer"))
        if shimmers:
            for golden_cookie in shimmers:
                try:
                    golden_cookie.click()
                    self.session.golden_cookies_clicked += 1
                except:
                    continue

    def check_store_upgrades(self):
        upgrades = self.driver.find_elements_by_class_name("enabled")
        if upgrades:
            for upgrade in upgrades:
                try:
                    upgrade.click()
                except:
                    continue

    def check_products_upgrades(self):
        self.products, index = [], 0
        while True:
            try:
                product = self.driver.find_element_by_id(f"product{index}")
                index += 1
                self.products.append(product)
            except:
                break

    def check_upgrades(self):
        levels = ("cookie", "cookies", "million", "billion", "trillion", "quadrillion",
                  "quintillion", "sextillion", "septillion", "octillion")
        cookie_text = self.cookie_count.text.split(" ")
        level = levels.index(cookie_text[1].split("\n")[0])
        amount = float("".join(cookie_text[0].split(",")))

        for product in self.products:
            element = product.text.split("\n")
            if len(element) > 1:
                product_text = element[1].split(" ")
                product_cost = float("".join(product_text[0].split(",")))

                if len(product_text) >= 2 and product_text[1] in levels:
                    product_level = levels.index(product_text[1])
                else:
                    product_level = -1
                if amount >= product_cost and level >= product_level:
                    product.click()

    async def actions(self):
        if self.iteration % 5 == 0:
            self.check_store_upgrades()
            self.check_products_upgrades()
            self.check_golden_cookies()
            self.close_pop_ups()
        self.cookie.click()
        self.check_upgrades()
        self.iteration += 1

    async def run(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Got it!"))
            ).click()
            self.grab_stats(False)
            self.change_bakery_name()
            if not self.controlled:
                while True:
                    await self.actions()
        except Exception as error:
            Utils.text_to_speech("An error has occured!")
            Utils.colored_print(f"ERROR: {error}", color="red")

        if not self.controlled:
            self.grab_stats(True)
            self.session.save_session()
