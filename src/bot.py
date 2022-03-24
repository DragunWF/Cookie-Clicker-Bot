import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

from utils import Utils


class Bot:
    def __init__(self, session, settings):
        self.bakery_names = tuple(settings["bakery_names"])
        self.session = session

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get("https://orteil.dashnet.org/cookieclicker/")

        self.cookie = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "bigCookie"))
        )
        self.cookie_count = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "cookies"))
        )
        self.products = None

        sleep(3)

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
        self.pop_ups = self.driver.find_elements_by_class_name("close")
        for pop_up in self.pop_ups:
            try:
                pop_up.click()
            except:
                continue

    def check_golden_cookies(self):
        shimmers = self.driver.find_elements_by_class_name("shimmer")
        if len(shimmers):
            for golden_cookie in shimmers:
                golden_cookie.click()

    def check_store_upgrades(self):
        upgrades = self.driver.find_elements_by_class_name("enabled")
        if len(upgrades):
            for upgrade in upgrades:
                try:
                    upgrade.click()
                except:
                    continue

    def check_products_upgrades(self):
        self.products = []
        index = 0
        while True:
            try:
                self.products.append(
                    self.driver.find_element_by_id(f"product{index}"))
                index += 1
            except:
                break

    def check_upgrades(self):
        levels = ("cookie", "cookies", "million", "billion", "trillion", "quadrillion",
                  "quintillion", "sextillion", "septillion", "octillion")
        level = levels.index(
            self.cookie_count.text.split(" ")[1].split("\n")[0])
        amount = float(self.cookie_count.text.split(" ")[0])

        for product in self.products:
            element = product.text.split("\n")
            if len(element) > 1:
                product_cost = float("".join(element[1].split(",")))
                if len(element) > 2 and element[2] in levels:
                    product_level = levels.index(element[2])
                else:
                    product_level = -1
                if amount >= product_cost and level >= product_level:
                    product.click()

    def actions(self):
        self.action = ActionChains(self.driver)
        iteration = 0
        while True:
            if iteration % 5 == 0:
                self.check_store_upgrades()
                self.check_products_upgrades()
                self.check_golden_cookies()
                self.close_pop_ups()
            self.action.click(self.cookie)
            self.check_upgrades()

            iteration += 1
            self.action.perform()

    def run(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Got it!"))
            ).click()
            self.change_bakery_name()
            self.actions()
        except Exception as error:
            Utils.text_to_speech("An error has occured!")
            Utils.colored_print(f"ERROR: {error}", color="red")
