import os
from time import sleep

import requests


TOKEN = "02a48fc85823393c2c20c321febeffb8"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
BREAK = "\n\n=====\n\n"


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
    print("Enter City Name (should be in compliance to OpenWeatherMap's City Index) :")
    CITY = input()
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
    resp_PROD = requests.get(URL)
    if resp_PROD.status_code == 200:
        pass
    else:
        raise TypeError("Oops, wrong city name or code?")
        sleep(5)
        exit()

    breakliner()
    data = resp_PROD.json()
    print(data)
    breakliner()
    return data


OWMCITY()

exitQuery()
