
import selenium
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


file = "chromedriver.exe"
driver = webdriver.Chrome(file)

driver.get("https://www.klart.se/se/hallands-l%C3%A4n/v%C3%A4der-halmstad/")

iframe = driver.find_element_by_xpath("//iframe[contains(@id,'sp_message_iframe_502944')]")
driver.switch_to.frame(iframe)
cookieAccept = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Okej']")))
cookieAccept.click()

driver.switch_to.default_content()

goToWeather = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='js-close link']")))
goToWeather.click()

clickOnTodaysWeather = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "day-1")))
clickOnTodaysWeather.click()


times = {}

#time.sleep(6)

#driver.quit()       #closes driver