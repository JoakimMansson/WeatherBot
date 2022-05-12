import datetime
from typing import Tuple, List, Optional

import selenium
import time
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


file = "chromedriver.exe"
driver = webdriver.Chrome(file)
AvailableTimeTemps = {}

checkin_date = datetime.date.fromordinal(datetime.date.today().toordinal()-0).strftime("%Y-%m-%d")
checkout_date = datetime.date.fromordinal(datetime.date.today().toordinal()-0).strftime("%Y-%m-%d")
driver.get("https://www.klart.se/se/hallands-l%C3%A4n/v%C3%A4der-halmstad/")

iframe = driver.find_element_by_xpath("//iframe[contains(@id,'sp_message_iframe_502944')]")
driver.switch_to.frame(iframe)
cookieAccept = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Okej']")))
cookieAccept.click()

driver.switch_to.default_content()

goToWeather = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='js-close link']")))
goToWeather.click()

clickOnTodaysWeather = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.ID, "day-1")))
clickOnTodaysWeather.click()

dicHourTemp = {}
dicOddsRain = {}
for i in range(1,24):
    try:

        allHours = driver.find_element_by_xpath("//div[@id='hour-1_" + str(i) + "']"+"//*[@data-qa-id='hour-day-hour']").text                           #All hours
        allTemps = driver.find_element_by_xpath("//div[@id='hour-1_" + str(i) + "']"+"//*[@class='value']").text                                        #All temperatures
        allTemps = re.sub("°","", allTemps)

        allRainProb = driver.find_element_by_xpath("//div[@id='hour-1_" + str(i) + "']"+"//*[@class='col -precipitationProbablility']").text            #Probability of rain
        allRainProb = re.sub("%","",allRainProb)

        print(allHours + ": " + allTemps + " C")
        print(allHours + ": " + allRainProb + " %")

        dicHourTemp.update({allHours:int(allTemps)})
        dicOddsRain.update({allHours:int(allRainProb)})
    except:
        pass


def getThreeHighest(hour_optional: dict) -> Tuple[List[Optional[str]], List[int]]:

    maxInt = -999
    allTempsDic = {}
    for i in range(0, 23):
        try:
            temp = hour_optional.get(timeConvert(i))        #Gets temperature of current time
            allTempsDic.update({temp:timeConvert(i)})   #
            if temp > maxInt:
                maxInt = temp
        except:
            pass


    threeHighest = []
    threeCorresepondingHours = []
    counter = 0
    for i in range(maxInt, -30, -1):

        if counter == 3:
            break
        try:
            if allTempsDic.get(i) is not None:
                threeHighest.append(i)
                threeCorresepondingHours.append(allTempsDic.get(i))
                counter += 1
        except:
            pass

    print(threeCorresepondingHours)
    print(threeHighest)

    return threeCorresepondingHours, threeHighest



def timeConvert(integer: int) -> str:

    if integer < 10:
        return "0" + str(integer) + ":00"
    else:
        return str(integer) + ":00"


getThreeHighest(dicHourTemp)
getThreeHighest(dicOddsRain)

