from unittest import TestCase, main

from requests import get

TOKEN = "c439e1209216cc7e7c73a3a8d1d12bfd"
CITY = "Norway"  # test *only*
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
URL = BASE_URL + "q=" + CITY + "&appid=" + TOKEN
resp_PROD = get(URL)


class testAPILoad(TestCase):
    def test_data_processcode(self):
        data = resp_PROD.json()
        main = data["main"]
        main["humidity"]
        main["pressure"]
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


if __name__ == "__main__":
    main()
