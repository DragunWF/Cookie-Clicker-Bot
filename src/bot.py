import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from utils import Utils


class Bot:
    def __init__(self, session: object, settings: dict):
        self.__controlled = settings["controlled"]
        self.__bakery_names = tuple(settings["bakery_names"])
        self.__session = session

        self.__playing_from_save_file = settings["saves"]["load_save_file"]
        self.__session.save_file_loaded = self.__playing_from_save_file
        if self.__playing_from_save_file:
            self.__save_file_location = settings["save_file_location"]

        self.__driver = webdriver.Chrome(ChromeDriverManager().install())
        self.__driver.get("https://orteil.dashnet.org/cookieclicker/")
        self.__driver.maximize_window()

        self.__cookie = WebDriverWait(self.__driver, 60).until(
            EC.presence_of_element_located((By.ID, "bigCookie"))
        )
        self.__cookie_count = WebDriverWait(self.__driver, 60).until(
            EC.presence_of_element_located((By.ID, "cookies"))
        )
        self.__products = None
        self.__iteration = 0

        Utils.tts_print("Bot has been initialized", color="green")
        sleep(1)

    def grab_stats(self, session_ending: bool):
        stats_button = WebDriverWait(self.__driver, 60).until(
            EC.presence_of_element_located((By.ID, "statsButton"))
        )
        stats_button.click()

        stats = WebDriverWait(self.__driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "subsection"))
        )
        self.__session.save_session_stats(stats.text.split("\n"), session_ending)

        stats_button.click()

    def save_game(self):
        options_button = WebDriverWait(self.__driver, 60).until(
            EC.presence_of_element_located((By.ID, "prefsButton"))
        )
        options_button.click()
        WebDriverWait(self.__driver, 60).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Save to file"))
        ).click()
        options_button.click()

    def __load_save_file(self):
        options_button = WebDriverWait(self.__driver, 60).until(
            EC.presence_of_element_located((By.ID, "prefsButton"))
        )
        options_button.click()

        WebDriverWait(self.__driver, 60).until(
            EC.presence_of_element_located((By.ID, "FileLoadInput"))
        ).send_keys(self.__save_file_location)
        options_button.click()

    def __change_bakery_name(self):
        WebDriverWait(self.__driver, 60).until(
            EC.presence_of_element_located((By.ID, "bakeryName"))
        ).click()
        name_input = WebDriverWait(self.__driver, 60).until(
            EC.presence_of_element_located((By.ID, "bakeryNameInput"))
        )
        name_input.clear()
        name_input.send_keys(random.choice(self.__bakery_names))
        self.__driver.find_element_by_id("promptOption0").click()

    def __close_pop_ups(self):
        self.pop_ups = tuple(self.__driver.find_elements_by_class_name("close"))
        for pop_up in self.pop_ups:
            try:
                pop_up.click()
            except:
                continue

    def __check_golden_cookies(self):
        shimmers = tuple(self.__driver.find_elements_by_class_name("shimmer"))
        if shimmers:
            for golden_cookie in shimmers:
                try:
                    golden_cookie.click()
                except:
                    continue

    def __check_store_upgrades(self):
        upgrades = self.__driver.find_elements_by_class_name("enabled")
        if upgrades:
            for upgrade in upgrades:
                try:
                    upgrade.click()
                except:
                    continue

    def __check_products_upgrades(self):
        self.__products, index = [], 0
        while True:
            try:
                product = self.__driver.find_element_by_id(f"product{index}")
                index += 1
                self.__products.append(product)
            except:
                break

    def __check_upgrades(self):
        levels = ("cookie", "cookies", "million", "billion", "trillion", "quadrillion",
                  "quintillion", "sextillion", "septillion", "octillion")
        cookie_text = self.__cookie_count.text.split(" ")
        level = levels.index(cookie_text[1].split("\n")[0])
        amount = float("".join(cookie_text[0].split(",")))

        for product in self.__products:
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
        if self.__iteration % 5 == 0:
            self.__check_store_upgrades()
            self.__check_products_upgrades()
            self.__check_golden_cookies()
            self.__close_pop_ups()
        self.__cookie.click()
        self.__check_upgrades()
        self.__iteration += 1

    async def run(self):
        try:
            WebDriverWait(self.__driver, 60).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Got it!"))
            ).click()
            if not self.__playing_from_save_file:
                self.__change_bakery_name()
            else:
                self.__load_save_file()
            self.grab_stats(False)
            if not self.__controlled:
                while True:
                    await self.actions()
        except Exception as error:
            Utils.text_to_speech("An error has occured!")
            Utils.colored_print(f"ERROR: {error}", color="red")
