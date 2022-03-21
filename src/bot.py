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
        self.url = "https://orteil.dashnet.org/cookieclicker/"
        self.driver.get(self.url)

    def check_golden_cookies(self):
        pass

    def check_cookies(self):
        pass

    def check_upgrades(self):
        levels = ("cookie", "cookies", "million", "billion", "trillion", "quadrillion",
                  "quintillion", "sextillion", "septillion", "octillion")

        products = self.driver.find_elements_by_id("products")
        cookies_count = self.driver.find_element_by_id("cookies")
        sleep(0.1)
        level = cookies_count.text.split(" ")[1].split("\n")[0]
        amount = float(cookies_count.text.split(" ")[0])
        print(f"{amount} {level}")

        for product in products:
            if len(product.text):
                print(product.text)
                # product_level = levels.index(product.text.split(" ")[1])
                # product_cost = float(product.text.split(" ")[0])
                # print(f"Cost: {product_cost} {product_level}")
                # if amount >= product_cost and level >= product_level:
                #     product.click()

                # don't forget about splitting commas and joining them then converting them to float

    def click_cookie(self):
        self.cookie = self.driver.find_element_by_id("bigCookie")
        self.action.click(self.cookie)

    def actions(self):
        self.action = ActionChains(self.driver)
        while True:
            self.click_cookie()
            self.check_upgrades()
            self.action.perform()
            sleep(0.001)

    def run(self):
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, "bigCookie"))
        )
        self.actions()
