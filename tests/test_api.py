import os
import unittest
from time import sleep
import requests
from dotenv import load_dotenv

TOKEN = os.getenv("TOKEN")
print(TOKEN)
CITY = "Norway"  # test *only*
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
URL = BASE_URL + "q=" + CITY + "&appid=" + TOKEN
resp_PROD = requests.get(URL)


class testAPILoad(unittest.TestCase):
    load_dotenv()

    def test_request(self):
        TOKEN = os.getenv("TOKEN")
        if resp_PROD.status_code == 200:
            print(resp_PROD.status_code)
            pass
        else:
            raise TypeError("Oops, wrong city name or code?")
            sleep(5)
            exit()
    def test_data_processcode(self):
        TOKEN = os.getenv("TOKEN")
        data = resp_PROD.json()
        main = data["main"]
        humidity = main["humidity"]
        pressure = main["pressure"]
        temp = main['temp']
        temp_min = main['temp_min']
        temp_max = main['temp_max']
        def ktc(temp, temp_min, temp_max):
            temp = temp - 273.15
            temp_min = temp_min - 273.15
            temp_max = temp_max - 273.15
            print("Temperature: ", temp, "°C")
            print("Minimum Temperature: ", temp_min, "°C")
            print("Maximum Temperature: ", temp_max, "°C")
        print(ktc(temp, temp_min, temp_max))
        print(data['weather'][0]['main'])

        

if __name__ == "__main__":
    unittest.main()
