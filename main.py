from __future__ import annotations

from platform import system
from tkinter import Event, Menu, Tk, Toplevel, messagebox
from tkinter.ttk import Button, Entry, Frame, Label, Progressbar, Style

from pyowm import OWM
from pyowm.commons.exceptions import APIRequestError
from pyowm.commons.exceptions import NotFoundError as OWMNotFoundError
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
        self.app_menu.add_command(label="About Weather", command=self.about)
        self.config(menu=self.menubar)

        # Set up style
        Style().theme_use("clam")

        # Set up window
        self.title("Weather")
        self.resizable(False, False)
        self.configure(bg="white")

        # Set up widgets
        self.main_frame = Frame(self)
        self.main_frame.pack()

        heading = Label(self.main_frame, text="Weather", font="Helvetica 25 bold")
        heading.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.cityname = Label(self.main_frame, text="City: None", font=("Helvetica 15"))
        self.cityname.grid(row=1, column=0, columnspan=2)

        self.searchbar = Entry(self.main_frame, width=42)
        self.searchbar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.bind("<Return>", self.OWMCITY)

        self.info_frame = Frame(self.main_frame, relief="sunken")
        self.info_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.label_weather = Label(self.info_frame, text="", font=("Helvetica 13"))
        self.label_weather.grid(row=0, column=0, columnspan=2)

        self.label_temp = Label(self.info_frame, text="", font=("Helvetica 13"))
        self.label_temp.grid(row=1, column=0, columnspan=2)

        self.label_temp_max = Label(self.info_frame, text="", font=("Helvetica 13"))
        self.label_temp_max.grid(row=2, column=0, columnspan=2)

        self.label_temp_min = Label(self.info_frame, text="", font=("Helvetica 13"))
        self.label_temp_min.grid(row=3, column=0, columnspan=2)

        self.label_feels_like = Label(self.info_frame, text="", font=("Helvetica 13"))
        self.label_feels_like.grid(row=4, column=0, columnspan=2)

        self.label_humidity = Label(self.info_frame, text="", font=("Helvetica 13"))
        self.label_humidity.grid(row=5, column=0, columnspan=2)

        self.label_pressure = Label(self.info_frame, text="", font=("Helvetica 13"))
        self.label_pressure.grid(row=6, column=0, columnspan=2)

        self.label_visibility = Label(self.info_frame, text="", font=("Helvetica 13"))
        self.label_visibility.grid(row=7, column=0, columnspan=2)

        self.label_windspeed = Label(self.info_frame, text="", font=("Helvetica 13"))
        self.label_windspeed.grid(row=8, column=0, columnspan=2)

        # Set up buttons
        self.start_button = Button(
            self.main_frame, text="Search for City", command=self.OWMCITY
        )
        self.start_button.grid(row=12, column=0, padx=10, pady=10)
        Button(self.main_frame, text="Exit", command=self.exit_app).grid(
            row=12, column=1, padx=10, pady=10
        )

        # Set variables
        self.searching: bool = False

        # Resize and deiconify
        self.resize_app()
        self.deiconify()

    def about(self) -> None:
        """Display a messagebox with information about the app."""

        messagebox.showinfo(
            "About Weather",
            "Weather is a simple weather app that uses the OpenWeatherMap API to get the weather for a given city.",
            parent=self,
        )

    def resize_app(self) -> None:
        """Use tkinter to detect the minimum size of the app, get the center of the screen, and place the app there."""

        # Update widgets so minimum size is accurate
        self.update_idletasks()

        # Get minimum size
        minimum_width: int = self.winfo_reqwidth()
        minimum_height: int = self.winfo_reqheight()

        # Get center of screen based on minimum size
        x_coords = int(self.winfo_screenwidth() / 2 - minimum_width / 2)
        y_coords = int(self.wm_maxsize()[1] / 2 - minimum_height / 2)

        # Place app and make the minimum size the actual minimum size (non-infringable)
        self.geometry(f"{minimum_width}x{minimum_height}+{x_coords}+{y_coords}")
        self.wm_minsize(minimum_width, minimum_height)

    def exit_app(self) -> None:
        """Exit the app."""
        self.destroy()

    def OWMCITY(self, _: Event | None = None) -> None:
        """Get the weather for a given city using the OpenWeatherMap API and display it in a label."""

        # Check if already searching
        if self.searching:
            return
        self.searching = True

        # Start the Progress Bar, disable buttons and clear labels, and disable searchbar
        self.start_button.configure(state="disabled")
        self.searchbar.configure(state="disabled")
        self.update_labels()

        # Get API key
        api_key: str = "c439e1209216cc7e7c73a3a8d1d12bfd"
        owm = OWM(api_key)
        mgr = owm.weather_manager()
        # Get city name
        city: str = self.searchbar.get()
        self.searchbar.delete(0, "end")

        # Check if city is empty
        if not city:
            # TODO: Make a method to reduce code duplication (boilerplate)
            self.cityname.configure(text="City: Needs Name")
            self.update_labels()
            self.start_button.configure(state="normal")
            self.searchbar.configure(state="normal")
            self.searching = False
            self.resize_app()  # In case the name gets too long or it renders differently on other systems
            return

        # Check if city exists
        try:
            observation = mgr.weather_at_place(city)
        except OWMNotFoundError or APIRequestError:
            self.cityname.configure(text="City: Not Found")
            self.update_labels()
            self.start_button.configure(state="normal")
            self.searchbar.configure(state="normal")
            self.searching = False
            self.resize_app()  # In case the name gets too long or it renders differently on other systems
            return

        # Get weather data
        weather = observation.weather

        # Send request to OpenWeatherMap API
        response: Response = requests_get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        )

        # Check if request was successful
        if response.status_code != 200:
            self.cityname.configure(text="City: Connection Error")
            self.update_labels()
            self.start_button.configure(state="normal")
            self.searchbar.configure(state="normal")
            self.searching = False
            self.resize_app()  # In case the name gets too long or it renders differently on other systems
            return

        # Get response data, simplify and create variables for usage
        # TODO: Give all data in dual columns
        # | Weather: Clear    | Temp: 20°C |
        # TODO: Allow users to change between imperial and metric (Fahrenheit and Celsius)
        data = response.json()
        main = data["main"]
        temperature = weather.temperature("celsius")

        # Update labels
        self.update_labels(
            [
                f"Weather: {weather.status} ~ {weather.detailed_status}",
                f"Current Temperature: {temperature.get('temp', None):.2f}°C",
                f"Maximum Temperature: {temperature.get('temp_max', None):.2f}°C",
                f"Minimum Temperature: {temperature.get('temp_min', None):.2f}°C",
                f"Feels like {temperature.get('feels_like', None):.2f}°C",
                f"Humidity: {main['humidity']:.2f}%",
                f"Pressure: {main['pressure']:.2f} hPa",
                f"Visibility: {weather.visibility(unit='kilometers'):.2f} km",
                f"Wind Speed: { weather.wind(unit='meters_sec')['speed']:.2f} meters per second",
            ]
        )

        # Set the city name
        self.cityname.configure(text=f"City: {city}")

        # Stop the Progress Bar, enable buttons and searchbar, and set searching to False
        self.start_button.configure(state="normal")
        self.searchbar.configure(state="normal")
        self.searching = False
        self.resize_app()  # In case the name gets too long or it renders differently on other systems

    def update_labels(self, data: list[str] = ["" for _ in range(9)]) -> None:
        """Clear all weather labels."""

        self.label_weather.configure(text=data[0])
        self.label_temp.configure(text=data[1])
        self.label_temp_max.configure(text=data[2])
        self.label_temp_min.configure(text=data[3])
        self.label_feels_like.configure(text=data[4])
        self.label_humidity.configure(text=data[5])
        self.label_pressure.configure(text=data[6])
        self.label_visibility.configure(text=data[7])
        self.label_windspeed.configure(text=data[8])
        return None


if __name__ == "__main__":
    app = App()
    app.mainloop()
