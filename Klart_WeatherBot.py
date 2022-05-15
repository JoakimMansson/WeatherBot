import bisect
import datetime
import heapq
import time
from operator import itemgetter

import requests
import selenium
import re
import linecache
import numpy as np

from typing import Tuple, List, Optional

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



class Klart:

    def __init__(self, bot: str, botChatID: str, url: str):
        self.botToken = bot
        self.botChatID = botChatID
        self.__initializerChromeDriver()
        self.__goToWeather(url)


    def __initializerChromeDriver(self):
        file = "chromedriver.exe"
        self.driver = webdriver.Chrome(file)


    #@PARAM regionURL an url to your specific city (could be https://www.klart.se/se/hallands-l%C3%A4n/v%C3%A4der-halmstad/ which is Halmstads url)
    def __goToWeather(self, cityURL: str):
        self.driver.get(cityURL)

        time.sleep(0.3)
        iframe = self.driver.find_element_by_xpath("//iframe[contains(@id,'sp_message_iframe_502944')]")
        self.driver.switch_to.frame(iframe)
        cookieAccept = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Okej']")))
        cookieAccept.click()


        self.driver.switch_to.default_content()
        time.sleep(0.3)
        goToWeather = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='js-close link']")))
        goToWeather.click()

        time.sleep(0.3)
        clickOnTodaysWeather = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "day-1")))
        clickOnTodaysWeather.click()


    #
    #@PARAM className is a string that could be any of the
    #@RETURN a weatherStatistic dictionary
    #
    def fetchValues(self, className: str, subElement: str, toSubFor: str) -> dict:

        weatherStatDict = {}
        for i in range(1, 23):
            try:
                time.sleep(0.1)
                hours = self.driver.find_element_by_xpath("//div[@id='hour-1_" + str(i) + "']"+"//*[@data-qa-id='hour-day-hour']").text              #All hours
                weatherStat = self.driver.find_element_by_xpath("//div[@id='hour-1_" + str(i) + "']"+"//*[@class='" + className + "']").text
                weatherStat = re.sub(subElement, toSubFor, weatherStat)
                print(hours + ":" + weatherStat)
                weatherStatDict.update({hours:int(weatherStat)})
            except:
                pass

        return weatherStatDict


    #@PARAM hour_optional a dictionary that contains an hour (16:00, 20:00) and an integer value
    #@PARAM number the amount of different values you want to be returned
    #@PARAM start_hour the starting hour to get values from (must be between or equal to 0 and 24)
    #@PARAM end_hour when to stop fetching values (must be between or equal to 0 and 24)
    def get_N_Highest(self, inputDict: dict, nrValues: int, startHour: int, endHour: int) -> Tuple[List[str], List[float]]:

        if len(inputDict.keys()) == 0:
            return None

        valueList = []
        for key in inputDict:

            if len(valueList) == 0:
                valueList.append({key: inputDict.get(key)})

            else:
                check = False
                for i in range(len(valueList)):
                    if check:
                        break

                    for tempKey in valueList[i].keys():

                        if inputDict.get(key) <= inputDict.get(tempKey):
                            valueList.insert(i, {key:inputDict.get(key)})
                            check = True

                        if inputDict.get(key) > inputDict.get(tempKey):
                            while inputDict.get(key) > inputDict.get(tempKey) and i < len(valueList):
                                i += 1
                            valueList.insert(i+1, {key: inputDict.get(key)})
                            check = True


        highestValues = []
        CorrespondingHours = []
        counter = 0
        for i in range(len(valueList)-1, -1, -1):

            if counter == nrValues:
                break

            for key in valueList[i]:
                if startHour <= self.__timeToIntConvert(key) <= endHour:
                    highestValues.append(valueList[i].get(key))
                    CorrespondingHours.append(key)
                    counter += 1

        return CorrespondingHours, highestValues


    #@PARAM hour_optional a dictionary that contains an hour (16:00, 20:00) and an integer value
    #@PARAM number the amount of different values you want to be returned
    #@PARAM start_hour the starting hour to get values from (must be between or equal to 0 and 24)
    #@PARAM end_hour when to stop fetching values (must be between or equal to 0 and 24)
    def get_N_Lowest(self, inputDict: dict, nrValues: int, startHour: int, endHour: int) -> Tuple[List[str], List[float]]:

        if len(inputDict.keys()) == 0:
            return None


        valueList = []
        for key in inputDict:

            if len(valueList) == 0:
                valueList.append({key: inputDict.get(key)})

            else:
                check = False
                for i in range(len(valueList)):
                    if check:
                        break

                    for tempKey in valueList[i].keys():

                        if inputDict.get(key) <= inputDict.get(tempKey):
                            valueList.insert(i, {key: inputDict.get(key)})
                            check = True

                        if inputDict.get(key) > inputDict.get(tempKey):
                            while inputDict.get(key) > inputDict.get(tempKey) and i < len(valueList):
                                i += 1
                            valueList.insert(i + 1, {key: inputDict.get(key)})
                            check = True

        lowestValues = []
        CorrespondingHours = []
        counter = 0
        for i in range(len(valueList)):

            if counter == nrValues:
                break

            for key in valueList[i]:
                if startHour <= self.__timeToIntConvert(key) <= endHour:
                    lowestValues.append(valueList[i].get(key))
                    CorrespondingHours.append(key)
                    counter += 1

        return CorrespondingHours, lowestValues





    def getAverage(self, inputDict: dict, startHour: int, endHour: int):

        average = 0
        counter = 0
        for key in inputDict:
            currentTime = self.__timeToIntConvert(key)
            if startHour <= currentTime <= endHour:
                average += inputDict.get(key)
                counter += 1

        return average/counter


    def __timeToIntConvert(self, time: str) -> int:
        if time[0:1] == "0":
            return int(time[1:2])
        else:
            return int(time[0:2])


    def __intToTimeConvert(self, integer: int) -> str:
        if integer < 10:
            return "0" + str(integer) + ":00"
        else:
            return str(integer) + ":00"


    def __appendToList(self, dictionary: dict, value: int, hour: str):
        if dictionary.get(value) is None:
            dictionary[value] = []
            dictionary[value].append(hour)
        else:
            dictionary[value].append(hour)


    def send_notify(self, bot_message: str):
        send_text = 'https://api.telegram.org/bot' + self.botToken + '/sendMessage?chat_id=' + self.botChatID + '&parse_mode=Markdown&text=' + bot_message
        requests.get(send_text)



