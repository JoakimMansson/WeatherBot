import datetime
import time

import requests
import selenium
import re
import linecache

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

        iframe = self.driver.find_element_by_xpath("//iframe[contains(@id,'sp_message_iframe_502944')]")
        self.driver.switch_to.frame(iframe)
        cookieAccept = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Okej']")))
        cookieAccept.click()

        self.driver.switch_to.default_content()

        goToWeather = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='js-close link']")))
        goToWeather.click()

        clickOnTodaysWeather = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "day-1")))
        clickOnTodaysWeather.click()


    #
    #@PARAM className is a string that could be any of the
    #@RETURN a weatherStatistic dictionary
    #
    def fetchValues(self, className: str, subElement: str) -> dict:

        weatherStatDict = {}
        for i in range(1, 23):
            try:
                time.sleep(0.5)
                hours = self.driver.find_element_by_xpath("//div[@id='hour-1_" + str(i) + "']"+"//*[@data-qa-id='hour-day-hour']").text              #All hours
                weatherStat = self.driver.find_element_by_xpath("//div[@id='hour-1_" + str(i) + "']"+"//*[@class='" + className + "']").text
                weatherStat = re.sub(subElement, "", weatherStat)
                print(hours + ":" + weatherStat)
                weatherStatDict.update({hours:int(weatherStat)})
            except:
                break

        return weatherStatDict


    #@PARAM hour_optional a dictionary that contains an hour (16:00, 20:00) and an integer value
    #@PARAM number the amount of different values you want to be returned
    #@PARAM start_hour the starting hour to get values from (must be between or equal to 0 and 23)
    #@PARAM end_hour when to stop fetching values (must be between or equal to 0 and 23)
    def get_N_Highest(self, inputDict: dict, nrValues: int, start_hour: int, end_hour: int) -> Tuple[List[str], List[int]]:
        print("inne")
        maxInt = -9999
        valueDictionary = {}
        for i in range(start_hour, end_hour):     #In range of 06:00 to 21:00
            try:
                value = inputDict.get(self.__timeConvert(i))        #Gets temperature of current time
                valueDictionary.update({value: self.__timeConvert(i)})          #Flipping (XX:00:VAL) to (VAL:XX:00)
                if value > maxInt:
                    maxInt = value
            except:
                pass

        print("vidare")
        print(maxInt)
        HighestValues = []
        CorresepondingHours = []
        counter = 0
        for i in range(maxInt, -30, -1):

            if counter == nrValues:
                break
            try:
                if valueDictionary.get(i) is not None:
                    HighestValues.append(i)
                    CorresepondingHours.append(valueDictionary.get(i))
                    print(i)
                    counter += 1
            except Exception as e:
                pass


        return CorresepondingHours, HighestValues


    #@PARAM hour_optional a dictionary that contains an hour (16:00, 20:00) and an integer value
    #@PARAM number the amount of different values you want to be returned
    #@PARAM start_hour the starting hour to get values from (must be between or equal to 0 and 23)
    #@PARAM end_hour when to stop fetching values (must be between or equal to 0 and 23)
    def get_N_Lowest(self, inputDict: dict, nrValues: int, start_hour: int, end_hour: int) -> Tuple[List[str], List[int]]:

        minInt = 9999
        valueDictionary = {}
        for i in range(start_hour, end_hour):                              #In range of 06:00 to 21:00
            try:
                value = inputDict.get(self.__timeConvert(i))    #Gets temperature of current time
                valueDictionary.update({value: self.__timeConvert(i)})  #Puts temperature in a dictonary (3: 13:00)
                if value < minInt:
                    minInt = value
            except:
                pass

        print(minInt)
        LowestValues = []
        CorrespondingHours = []
        counter = 0
        for i in range(minInt, 100, 1):

            if counter == nrValues:
                break
            try:
                if valueDictionary.get(i) is not None:
                    LowestValues.append(i)
                    CorrespondingHours.append(valueDictionary.get(i))
                    print(i)
                    counter += 1
            except:
                pass


        return CorrespondingHours, LowestValues


    def __timeConvert(self, integer: int) -> str:

        if integer < 10:
            return "0" + str(integer) + ":00"
        else:
            return str(integer) + ":00"


    def send_notify(self, bot_message: str):
        send_text = 'https://api.telegram.org/bot' + self.botToken + '/sendMessage?chat_id=' + self.botChatID + '&parse_mode=Markdown&text=' + bot_message
        requests.get(send_text)




if __name__ == "__main__":
    botToken = re.sub("\n", "", linecache.getline("Credentials", 4))
    chatID = re.sub("\n", "", linecache.getline("Credentials", 7))

    weather = Klart(botToken, chatID, "https://www.klart.se/se/hallands-l%C3%A4n/v%C3%A4der-halmstad/")

    temperature = weather.fetchValues("col -temp","°")
    rainProbability = weather.fetchValues("col -precipitationProbablility", "%")
    miliRainExpected = weather.fetchValues("col -precipitation", "")

    #ThreeHighestTemps = weather.get_N_Highest(temperature, 3, 0, 23)
    HighestTemp = weather.get_N_Highest(temperature, 1, 0, 24)
    HighestRainProb = weather.get_N_Highest(rainProbability, 1, 0, 24)
    ThreeHighestMiliRain = weather.get_N_Highest(miliRainExpected, 3, 0, 24)
    if ThreeHighestMiliRain != None:

        weather.send_notify(
            "Highest temp today: " + HighestTemp[0][0] + " -> " + str(HighestTemp[1][0]) + " C° 🔆" + "\n"
            "Highest probability of rain: " + HighestRainProb[0][0] + " -> " + str(HighestRainProb[1][0]) + "% 💧" + "\n"
            "Rain expected: "
        )
    else:
        "Highest temp today: " + HighestTemp[0][0] + " -> " + str(HighestTemp[1][0]) + " C° 🔆" + "\n"
        "Highest probability of rain: " + HighestRainProb[0][0] + " -> " + str(HighestRainProb[1][0]) + "% 💧" + "\n"
        "No rain expected!! 😄"






