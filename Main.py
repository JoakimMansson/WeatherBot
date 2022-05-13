import linecache
import re

from Klart_WeatherBot import Klart

if __name__ == "__main__":
    botToken = re.sub("\n", "", linecache.getline("Credentials", 4))
    chatID = re.sub("\n", "", linecache.getline("Credentials", 7))

    weather = Klart(botToken, chatID, "https://www.klart.se/se/hallands-l%C3%A4n/v%C3%A4der-halmstad/")

    temperature = weather.fetchValues("col -temp","°", "")
    rainProbability = weather.fetchValues("col -precipitationProbablility", "%", "")
    miliRainExpected = weather.fetchValues("col -precipitation", ",", ".")

    HighestTemp = weather.get_N_Highest(temperature, 1, 0, 24)
    HighestRainProb = weather.get_N_Highest(rainProbability, 1, 0, 24)
    HighestMiliRain = weather.get_N_Highest(miliRainExpected, 1, 0, 24)

    ThreeLowestTemps = weather.get_N_Lowest(temperature, 3, 0, 24)
    print("HEJ: " + ThreeLowestTemps[0][0] + str(ThreeLowestTemps[1][0]))
    print("HEJ: " + ThreeLowestTemps[0][1] + str(ThreeLowestTemps[1][1]))
    print("HEJ: " + ThreeLowestTemps[0][2] + str(ThreeLowestTemps[1][2]))

    print("Rain amount: \n" + HighestMiliRain[0][0] + " -> " + str(HighestMiliRain[1][0]) + " (mm) 💧" + "\n")
    if HighestRainProb[1][0] > 10:

        weather.send_notify(
            "Highest temp today: \n" + HighestTemp[0][0] + " -> " + str(HighestTemp[1][0]) + " C° 🔆" + "\n"
            "Highest probability of rain: \n" + HighestRainProb[0][0] + " -> " + str(HighestRainProb[1][0]) + "% 💧" + "\n"
        )
    else:
        weather.send_notify(
            "Highest temp today: \n" + HighestTemp[0][0] + " -> " + str(HighestTemp[1][0]) + " C° 🔆" + "\n"
            "Highest probability of rain: \n" + HighestRainProb[0][0] + " -> " + str(HighestRainProb[1][0]) + "% 💧" + "\n"
            "No rain expected!! 😄"
        )
