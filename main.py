import os
import sys
from time import sleep
from tkinter import *
from tkinter import ttk

import requests

TOKEN = "c439e1209216cc7e7c73a3a8d1d12bfd"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
BREAK = "\n\n=====\n\n"
# TOKEN = os.getenv("TOKEN")


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

    CITY = data["name"]
    sys = data["sys"]
    country = sys["country"]
    CITY2 = CITY + "," + " " + country
    if CITY == CITY2:
        pass
    else:
        CITY = data["name"]
        sys = data["sys"]
        country = sys["country"]
        CITY2 = CITY + "," + " " + country

    w_main = data["weather"][0]["main"]
    w_desc = data["weather"][0]["description"]
    pressure = main["pressure"]
    visibility = data["visibility"]
    visibility_new = visibility / 1000
    wind = data["wind"]["speed"]

    def printData():
        breakliner()
        print(f"{CITY2:-^30}")
        print(f"Weather: {w_main}:- {w_desc}")
        ktc(temp, temp_min, temp_max)
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")
        print(f"Wind speed: {wind} m/s")
        print(f"Visibility: {visibility} m (or) {visibility_new} km")

    printData()


def OWMCITY():
    # City Name request
    global CITY
    CITY = searchbar.get()
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

    global data
    data = resp_PROD.json()

    data_processing()
    exitQuery()


root = Tk()


root.geometry("700x250")

heading = Label(root, text="Weather", font="Helvetica 13").place(relx=0.5, rely=0.1, anchor=CENTER)

searchbar = Entry(root, width=42)
searchbar.place(relx=0.5, rely=0.5, anchor=CENTER)


label = Label(root, text="", font=("Helvetica 13"))
label.pack()


ttk.Button(root, text="Search for City", command=OWMCITY).place(
    relx=0.7, rely=0.5, anchor=CENTER
)

root.mainloop()
