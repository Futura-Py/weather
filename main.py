from __future__ import annotations

from platform import system
from tkinter import Menu, Tk, messagebox
from tkinter.ttk import Button, Entry, Frame, Label

from pyowm import OWM
from requests import Response
from requests import get as requests_get


class App(Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        # Set up Menubar
        if system() == "Darwin":
            self.menubar = Menu(self)
            # Apple menus have special names and special commands
            self.app_menu = Menu(self.menubar, tearoff=0, name="apple")
            self.menubar.add_cascade(label="App", menu=self.app_menu)
        else:
            self.menubar = Menu(self)
            self.app_menu = Menu(self.menubar, tearoff=0)
            self.menubar.add_cascade(label="App", menu=self.app_menu)
        self.menubar.add_command(label="About Weather", command=self.about)
        self.config(menu=self.menubar)

        # Set up window
        self.title("Weather")
        self.resizable(False, False)
        self.configure(bg="white")

        # Set up widgets
        self.main_frame = Frame(self, padding=10)
        self.main_frame.pack()

        heading = Label(self.main_frame, text="Weather", font="Helvetica 13")
        heading.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.cityname = Label(self.main_frame, text="", font=("Helvetica 13"))
        self.cityname.grid(row=1, column=0, columnspan=2)

        self.searchbar = Entry(self.main_frame, width=42)
        self.searchbar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.label_status = Label(
            self.main_frame, text="", font=("Helvetica 13"))
        self.label_status.grid(row=3, column=0, columnspan=2)

        self.label_temp = Label(
            self.main_frame, text="", font=("Helvetica 13"))
        self.label_temp.grid(row=4, column=0, columnspan=2)

        self.label_temp_max = Label(
            self.main_frame, text="", font=("Helvetica 13"))
        self.label_temp_max.grid(row=5, column=0, columnspan=2)

        self.label_temp_min = Label(
            self.main_frame, text="", font=("Helvetica 13"))
        self.label_temp_min.grid(row=6, column=0, columnspan=2)

        self.label_feels_like = Label(
            self.main_frame, text="", font=("Helvetica 13"))
        self.label_feels_like.grid(row=7, column=0, columnspan=2)

        self.label_humidity = Label(
            self.main_frame, text="", font=("Helvetica 13"))
        self.label_humidity.grid(row=8, column=0, columnspan=2)

        self.label_pressure = Label(
            self.main_frame, text="", font=("Helvetica 13"))
        self.label_pressure.grid(row=9, column=0, columnspan=2)

        self.label_visibility = Label(
            self.main_frame, text="", font=("Helvetica 13"))
        self.label_visibility.grid(row=10, column=0, columnspan=2)

        self.label_windspeed = Label(self.main_frame, text="", font=("Helvetica 13"))
        self.label_windspeed.grid(row=11, column=0, columnspan=2)
        Button(self.main_frame, text="Search for City", command=self.OWMCITY).grid(
            row=12, column=0, padx=10, pady=10
        )
        Button(self.main_frame, text="Exit", command=self.exit_app).grid(
            row=12, column=1, padx=10, pady=10
        )

        self.resize_app()
        self.deiconify()

    def about(self) -> App:
        """Display a messagebox with information about the app."""
        messagebox.showinfo(
            "About Weather",
            "Weather is a simple weather app that uses the OpenWeatherMap API to get the weather for a given city.",
            parent=self,
        )
        return self

    def resize_app(self) -> App:
        """Use tkinter to detect the minimum size of the app, get the center of the screen, and place the app there."""
        # Update widgets so minimum size is accurate
        self.update_idletasks()

        # Get minimum size
        minimum_width: int = self.winfo_reqwidth()
        minimum_height: int = self.winfo_reqheight()

        # Get center of screen based on minimum size
        x_coords = int(self.winfo_screenwidth() / 2 - minimum_width / 2)
        y_coords = int(self.winfo_screenheight() / 2 - minimum_height / 2) - 20
        # `-20` should deal with Dock on macOS and looks good on other OS's

        # Place app and make the minimum size the actual minimum size (non-infringable)
        self.geometry(
            f"{minimum_width}x{minimum_height}+{x_coords}+{y_coords}")
        self.wm_minsize(minimum_width, minimum_height)
        return self

    def exit_app(self) -> None:
        """Exit the app."""
        self.destroy()

    def OWMCITY(self) -> App:
        """Get the weather for a given city using the OpenWeatherMap API and display it in a label."""
        # Get API key
        api_key: str = "c439e1209216cc7e7c73a3a8d1d12bfd"
        owm = OWM(api_key)
        mgr = owm.weather_manager()
        # Get city name
        city: str = self.searchbar.get()
        observation = mgr.weather_at_place(city)
        weather = observation.weather
        # Send request to OpenWeatherMap API
        response: Response = requests_get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        )
        if response.status_code != 200:
            self.label_status.configure(text="City not found")
            return
        # Get response data, simplify and create variables for usage
        data = response.json()
        main = data["main"]
        temperature = weather.temperature("celsius")
        wind = weather.wind(unit='meters_sec')
        # Get temperature in Celsius
        # temperature_kelvin: float = main["temp"]
        # temperature_celsius = temperature_kelvin - 273.15
        temp = temperature.get("temp", None)
        temp_max = temperature.get("temp_max", None)
        temp_min = temperature.get("temp_min", None)
        feels_like = temperature.get("feels_like", None)
        status: str = weather.status
        detailed_status: str = weather.detailed_status
        # Other data needed from the API
        humidity = main["humidity"]
        pressure = main["pressure"]
        visibility = weather.visibility(unit='kilometers')
        windspeed: float = wind["speed"]
        # Put in label
        self.cityname.configure(text=data["name"] + ", " + data["sys"]["country"])
        self.label_status.configure(
            text="Weather: " + status + ":- " + detailed_status)
        self.label_temp.configure(text="Temperature: " + f"{temp:.2f}°C")
        self.label_temp_max.configure(
            text="Maximum Temperature: " + f"{temp_max:.2f}°C"
        )
        self.label_temp_min.configure(
            text="Minimum Temperature: " + f"{temp_min:.2f}°C"
        )
        self.label_feels_like.configure(
            text="Feels like " + f"{feels_like:.2f}°C")
        self.label_humidity.configure(text="Humidity: " + f"{humidity:.2f}%")
        self.label_pressure.configure(
            text="Pressure: " + f"{pressure:.2f}" + " hPa"
        )
        self.label_visibility.configure(
            text="Visibility: " + f"{visibility:.2f}" + " km")
        self.label_windspeed.configure(text="Wind Speed: " + f"{windspeed:.2f}" + " meters per second")
        return self


if __name__ == "__main__":
    app = App()
    app.mainloop()
