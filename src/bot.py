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
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get("https://orteil.dashnet.org/cookieclicker/")

    def define_element_variables(self):
        self.cookie = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "bigCookie"))
        )
        self.cookie_count = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "cookies"))
        )
        self.products = self.driver.find_elements_by_id("product0")

        sleep(3)

    def close_pop_ups(self):
        self.pop_ups = self.driver.find_elements_by_class_name("close")
        for pop_up in self.pop_ups:
            try:
                pop_up.click()
            except:
                continue

    def check_golden_cookies(self):
        pass

    def check_products(self):
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
                self.check_products()
            if iteration % 50 == 0:
                self.close_pop_ups()
            self.action.click(self.cookie)
            self.check_upgrades()

            iteration += 1
            self.action.perform()
            sleep(0.000001)

    def run(self):
        try:
            self.define_element_variables()
            cookie_pop_up = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Got it!"))
            )
            cookie_pop_up.click()
            self.actions()
        except Exception as error:
            Utils.text_to_speech("An error has occured!")
            Utils.colored_print(f"ERROR: {error}", color="red")
