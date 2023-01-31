import os
import sys
from time import sleep

import requests

TOKEN = "c439e1209216cc7e7c73a3a8d1d12bfd"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
BREAK = "\n\n=====\n\n"
TOKEN = os.getenv("TOKEN")


def breakliner():
    print(f"{BREAK:-^30}")
    return


def clearScreen():
    if sys.platform == "windows":
        os.system("cls")
    else:
        os.system("clear")
    return


def exitQuery():
    exitQ = input("Exit? ")
    if exitQ == "y":
        exit()
    elif exitQ == "n":
        clearScreen()
        OWMCITY()


def OWMCITY():
    # City Name request
    global CITY
    CITY = input(
        "Enter City Name (should be in compliance to OpenWeatherMap's City Index): "
    )
    if CITY == "exit":
        clearScreen()
        print("Three")
        sleep(1)
        clearScreen()
        print("Two")
        sleep(1)
        clearScreen()
        print("One.")
        sleep(1)
        clearScreen()
        print("Exiting...")
        sleep(0.5)
        exit()

    else:
        pass
    # The URL in actuality be like:
    URL = BASE_URL + "q=" + CITY + "&appid=" + TOKEN

    # PROD: Request Response
    global resp_PROD
    resp_PROD = requests.get(URL)
    if resp_PROD.status_code == 200:
        pass
    else:
        raise TypeError("Oops, wrong city name or code?")

    breakliner()
    global data
    data = resp_PROD.json()
    print(data)
    breakliner()


OWMCITY()


def data_processing():
    main = data["main"]
    humidity = main["humidity"]
    pressure = main["pressure"]
    temp = main["temp"]
    temp_min = main["temp_min"]
    temp_max = main["temp_max"]

    def ktc(temp, temp_min, temp_max):
        temp = temp - 273.15
        temp_min = temp_min - 273.15
        temp_max = temp_max - 273.15
        print("Temperature: ", temp, "°C")
        print("Minimum Temperature: ", temp_min, "°C")
        print("Maximum Temperature: ", temp_max, "°C")

    print(ktc(temp, temp_min, temp_max))
    print(data["weather"][0]["main"])


data_processing()


exitQuery()
