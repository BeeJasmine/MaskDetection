#test.py

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.remote.remote_connection import RemoteConnection
from time import sleep
import requests
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='class')
def driver(request):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    request.cls.driver = driver
    yield
    #driver.close()


@pytest.mark.usefixtures('driver')
class Test_api:
    pass

class Test_url(Test_api):

    # def subscribtion(self):
    #     self.driver.get('http://localhost:8501/')
    #     sleep(1)
    #     show_btn="/html/body/div/div[1]/div/div/div/div/section[1]/div[1]"
    #     self.driver.find_element_by_xpath(show_btn).click()
    #     #show_btn_inscription="/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[1]"
    #     btn_inscription_page='//*[@id="bui-26"]'
    #     self.driver.find_element_by_xpath(btn_inscription_page).click()
    #     field_username="/html/body/div/div[1]/div/div/div/div/section[2]/div/div[1]/div[4]/div/div[1]/div/input"
    #     self.driver.find_element_by_xpath(field_username).send_keys("Admin")
    #     field_password="/html/body/div/div[1]/div/div/div/div/section[2]/div/div[1]/div[5]/div/div[1]/div/input"
    #     self.driver.find_element_by_xpath(field_password).send_keys("S3curity!")
    #     btn_pp="/html/body/div/div[1]/div/div/div/div/section[2]/div/div[1]/div[6]/div/section/button"
    #     self.driver.find_element_by_xpath(btn_pp).click()

    #    uploader=

    #    .send_keys(os.getcwd()+"/image.png")


    #     btn_connect="/html/body/div/div[1]/div/div/div/div/section[2]/div/div[1]/div[8]/div/button"
    #     self.driver.find_element_by_xpath(btn_connect).click()
    #     sleep(2)

    def test_login(self):
        self.driver.get('http://localhost:8501/')
        sleep(2)
        input_username = "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[3]/div/div[1]/div/input"
        input_pwd = "/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[4]/div/div[1]/div/input"
        self.driver.find_element_by_xpath(input_username).send_keys("Admin")
        self.driver.find_element_by_xpath(input_pwd).send_keys("S3curity!")
        sleep(2)
        checkbox_login="/html/body/div/div[1]/div/div/div/div/section[1]/div[1]/div[2]/div[1]/div[5]/div/label/span"
        self.driver.find_element_by_xpath(checkbox_login).click()
        sleep(2)

