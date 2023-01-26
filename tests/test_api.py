import os
import unittest
from time import sleep

import requests
from dotenv import load_dotenv


class testAPILoad(unittest.TestCase):
    load_dotenv()

    def test_token(self):
        TOKEN = os.getenv("TOKEN")
        print(TOKEN)
        return TOKEN

    def test_request(self):
        CITY = "Norway"  # test *only*
        TOKEN = os.getenv("TOKEN")
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        URL = BASE_URL + "q=" + CITY + "&appid=" + TOKEN
        resp_PROD = requests.get(URL)
        if resp_PROD.status_code == 200:
            print(resp_PROD.status_code)
            pass
        else:
            raise TypeError("Oops, wrong city name or code?")
            sleep(5)
            exit()


if __name__ == "__main__":
    unittest.main()
