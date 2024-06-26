from __future__ import annotations

from pathlib import Path
from platform import system
from tkinter import Event, Menu, PhotoImage, TclError, Tk, Toplevel, messagebox
from tkinter.ttk import Button, Combobox, Entry, Frame, Label
from webbrowser import open as openwebpage

from platformdirs import user_data_dir
from pyowm import OWM
from pyowm.commons.exceptions import APIRequestError, InvalidSSLCertificateError
from pyowm.commons.exceptions import NotFoundError as OWMNotFoundError
from pyowm.commons.exceptions import TimeoutError
from requests import Response
from requests import get as requests_get
from sv_ttk import set_theme

from dialogs import Messagebox

VERSION = "0.1"

# Create constant
SYSTEM = system()

# Get file info
data_dir = Path(user_data_dir("Weather", "Futura-Py", ensure_exists=True))
data_file = Path(str(data_dir / "data.txt"))

# Ensure file directory exists
if not data_dir.exists():
    # Create the directory if it doesn't exist
    data_dir.mkdir(parents=True)
    data_file.touch()
    with open(data_file, "r+") as file:
        file.write("dark\nmetric")

# Ensure file exists and contains the correct data
if data_file.exists():
    # Ensure the file contains everything it needs
    # NOTE: File clearing has caused issues in the past so its better to
    # take the safe route and be very sure the file is cleared hence three
    # clearing methods instead of one
    with open(data_file, "r+") as f:
        data = f.read().splitlines()
        if len(data) != 2:
            # Clear the file and write the default values
            f.truncate(0)
            f.flush()
            f.seek(0)
            f.write("dark\nmetric")
            f.close()
        else:
            # Ensure the file contains the correct values
            if data[0] not in ["light", "dark"] or data[1] not in [
                "metric",
                "imperial",
            ]:
                # Clear the file and write the default values
                f.truncate(0)
                f.flush()
                f.seek(0)
                f.write("dark\nmetric")
                f.close()
            else:
                # File is good
                f.close()
else:
    # Write the file if it doesn't exist
    data_file.write_text("dark\nmetric")


class App(Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()

        # Set up Menubar
        if SYSTEM == "Darwin":
            self.menubar = Menu(self)

            # Apple menus have special names and special commands
            self.app_menu = Menu(self.menubar, tearoff=0, name="apple")
            self.menubar.add_cascade(label="App", menu=self.app_menu)
        else:
            self.menubar = Menu(self)
            self.app_menu = Menu(self.menubar, tearoff=0)
            self.menubar.add_cascade(label="App", menu=self.app_menu)
        self.app_menu.add_command(label="About Weather", command=self.about)
        self.app_menu.add_command(label="Settings", command=self.settings_window)
        self.config(menu=self.menubar)

        # Get file info
        with open(data_file, "r") as file:
            data = file.read().splitlines()
            self.color_mode = data[0]
            self.units = data[1]

        # Set up style
        set_theme(self.color_mode)

        # Set up window
        self.title("Weather")
        self.resizable(False, False)
        self.configure(bg="white")

        # Set up icon
        try:
            if SYSTEM == "darwin":
                self.iconbitmap("./assets/icon.icns")
            elif SYSTEM == "Windows":
                self.iconbitmap("./assets/icon.ico")
            else:
                logo_img = PhotoImage(file="./assets/icon.png")
                self.iconphoto(False, logo_img)
        except TclError:
            try:
                self.iconphoto("./assets/icon.ico")  # type: ignore
            except TclError:
                pass

        # Set up widgets
        self.main_frame = Frame(self)
        self.main_frame.grid()

        heading = Label(self.main_frame, text="Weather", font="Helvetica 25 bold")
        heading.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.cityname = Label(
            self.main_frame, text="City: None", font=("Helvetica 15 bold")
        )
        self.cityname.grid(row=2, column=0, columnspan=2)

        self.searchbar = Entry(self.main_frame, width=42)
        self.searchbar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.bind("<Return>", self.owm_search)

        # Set up buttons
        buttons_frame = Frame(self.main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="n")

        self.start_button = Button(
            buttons_frame, text="Search", command=self.owm_search
        )
        self.start_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        Button(
            buttons_frame,
            text="Exit",
            command=self.destroy,
        ).grid(row=0, column=1, padx=10, pady=10, sticky="e")
        self.info_frame = Frame(self.main_frame, relief="sunken")
        self.info_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

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

        # Set variables
        self.searching: bool = False

        # Resize, deiconify and check for updates
        self.resize_app()
        self.deiconify()
        self.update_idletasks()
        self.after_idle(lambda: self.check_for_updates())

    def settings_window(self) -> None:
        self.settings = Toplevel()
        self.settings.withdraw()
        settings_frame = Frame(self.settings)
        settings_frame.grid(row=0, column=0, padx=(0, 10), pady=(10, 0), sticky="w")
        self.units_label = Label(settings_frame, text="Units: ").grid(row=0, column=0)
        self.unit_combobox = Combobox(
            settings_frame,
            values=["Metric", "Imperial"],
            state="readonly",
            font=("Helvetica 13"),
            width=10,
        )
        self.unit_combobox.grid(row=0, column=2, padx=(0, 10), sticky="e")
        self.unit_combobox.current(0 if self.units == "metric" else 1)
        self.unit_combobox.bind("<<ComboboxSelected>>", self.update_settings)

        self.color_mode_label = Label(settings_frame, text="Color Mode: ").grid(
            row=2, column=0
        )
        self.color_mode_combobox = Combobox(
            settings_frame,
            values=["Light", "Dark"],
            state="readonly",
            font=("Helvetica 13"),
            width=10,
        )
        self.color_mode_combobox.grid(row=2, column=2, sticky="e")
        self.color_mode_combobox.current(0 if self.color_mode == "light" else 1)
        self.color_mode_combobox.bind("<<ComboboxSelected>>", self.update_settings)

        buttons = Frame(self.settings)
        buttons.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="n")

        Button(
            buttons,
            text="Exit",
            command=self.settings.destroy,
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.resize_app()
        self.settings.focus()
        self.settings.attributes("-topmost", "true")
        self.settings.deiconify()

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

    def reset_app(self, data: list[str] = ["" for _ in range(9)]) -> None:
        """Reset the app to its initial state."""

        # Update labels
        self.update_labels(data)

        # Reset variables
        self.searching = False

        # Reset widgets
        self.searchbar.configure(state="normal")
        self.start_button.configure(state="normal")

        # Resize app
        self.resize_app()

    def owm_search(self, _: Event | None = None) -> None:
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

        # Check if city is empty
        if not city:
            self.cityname.configure(text="City: Needs Name")
            self.reset_app()
            return

        # Removing redundancy
        def failed_weather_request() -> None:
            self.cityname.configure(text="City: Not Found")
            self.reset_app()

        # Check if city exists
        try:
            observation = mgr.weather_at_place(city)
        except (
            OWMNotFoundError
            or APIRequestError
            or TimeoutError
            or InvalidSSLCertificateError
        ):
            failed_weather_request()
            return

        # Check that observation is not None
        if observation is None:
            failed_weather_request()
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
            # In case the name gets too long or it renders differently on other systems
            self.resize_app()
            return

        # Get response data, simplify and create variables for usage
        # TODO: Give all data in dual columns (there's unused data!)
        # | Weather: Clear    | Temp: 20°C |
        data = response.json()
        main = data["main"]
        temperature = weather.temperature("celsius")

        # Update labels
        info: list[str] = (
            [
                f"Weather: {weather.status} ~ {weather.detailed_status}",
                f"Current Temperature: {temperature.get('temp', None):.2f}°C",
                f"Maximum Temperature: {temperature.get('temp_max', None):.2f}°C",
                f"Minimum Temperature: {temperature.get('temp_min', None):.2f}°C",
                f"Feels like {temperature.get('feels_like', None):.2f}°C",
                f"Humidity: {main['humidity']:.2f}%",
                f"Pressure: {main['pressure']:.2f} hPa",
                f"Visibility: {weather.visibility(unit='kilometers'):.2f} km",
                f"Wind Speed: {weather.wind(unit='meters_sec')['speed']:.2f} meters per second",
            ]
            if self.units == "metric"
            else [
                f"Weather: {weather.status} ~ {weather.detailed_status}",
                f"Current Temperature: {(temperature.get('temp', None)*(9/5))+32:.2f}°F",
                f"Maximum Temperature: {(temperature.get('temp_max', None)*(9/5))+32:.2f}°F",
                f"Minimum Temperature: {(temperature.get('temp_min', None)*(9/5))+32:.2f}°F",
                f"Feels like {(temperature.get('feels_like', None)*(9/5))+32:.2f}°F",
                f"Humidity: {main['humidity']:.2f}%",
                f"Pressure: {main['pressure']*.0145038:.2f} psi",
                f"Visibility: {weather.visibility(unit='miles'):.2f} miles",
                f"Wind Speed: {weather.wind(unit='miles_hour')['speed']:.2f} miles per hour",
            ]
        )

        # Set the city name
        self.cityname.configure(text=f"City: {data['name']}, {data['sys']['country']}")

        # Reset app
        self.reset_app(info)
        self.searchbar.delete(0, "end")

    def update_labels(self, data: list[str] = ["" for _ in range(9)]) -> None:

        self.label_weather.configure(text=data[0])
        self.label_temp.configure(text=data[1])
        self.label_temp_max.configure(text=data[2])
        self.label_temp_min.configure(text=data[3])
        self.label_feels_like.configure(text=data[4])
        self.label_humidity.configure(text=data[5])
        self.label_pressure.configure(text=data[6])
        self.label_visibility.configure(text=data[7])
        self.label_windspeed.configure(text=data[8])

    def update_settings(self, _: Event | None = None) -> None:
        """Updates the settings such as units and color mode"""

        # Color Mode Settings
        if self.color_mode == "light" and self.color_mode_combobox.get() == "Dark":
            set_theme("dark")
            self.color_mode = "dark"
            self.write_file()

        if self.color_mode == "dark" and self.color_mode_combobox.get() == "Light":
            set_theme("light")
            self.color_mode = "light"
            self.write_file()

        # Unit Settings
        if self.units == "metric" and self.unit_combobox.get() == "Imperial":
            self.units = "imperial"
            if not self.label_weather.cget(
                "text"
            ):  # Check that there is data to convert
                return
            self.update_labels(
                [
                    self.label_weather.cget("text"),
                    f"Current Temperature: {(float(self.label_temp.cget('text').split('°')[0].split(': ')[1]))*(9/5)+32:.2f}°F",  # noqa: E501
                    f"Maximum Temperature: {(float(self.label_temp_max.cget('text').split('°')[0].split(': ')[1]))*(9/5)+32:.2f}°F",  # noqa: E501
                    f"Minimum Temperature: {(float(self.label_temp_min.cget('text').split('°')[0].split(': ')[1])*(9/5))+32:.2f}°F",  # noqa: E501
                    f"Feels like {float(self.label_feels_like.cget('text').split('°')[0].split(' ')[2])*(9/5)+32:.2f}°F",
                    self.label_humidity.cget("text"),
                    f"Pressure: {float(self.label_pressure.cget('text').split(' ')[1])*.0145038:.2f} psi",
                    f"Visibility: {float(self.label_visibility.cget('text').split(' ')[1])*0.621371:.2f} miles",
                    f"Wind Speed: {float(self.label_windspeed.cget('text').split(' ')[2])*0.621371:.2f} miles per hour",
                ]
            )
            self.write_file()

        if self.units == "imperial" and self.unit_combobox.get() == "Metric":
            self.units = "metric"
            if not self.label_weather.cget(
                "text"
            ):  # Check that there is data to convert
                return
            self.update_labels(
                [
                    self.label_weather.cget("text"),
                    f"Current Temperature: {(5/9)*((float(self.label_temp.cget('text').split('°')[0].split(': ')[1])-32)):.2f}°C",  # noqa: E501
                    f"Maximum Temperature: {(5/9)*((float(self.label_temp_max.cget('text').split('°')[0].split(': ')[1])-32)):.2f}°C",  # noqa: E501
                    f"Minimum Temperature: {(5/9)*((float(self.label_temp_min.cget('text').split('°')[0].split(': ')[1])-32)):.2f}°C",  # noqa: E501
                    f"Feels like {(5/9)*((float(self.label_feels_like.cget('text').split('°')[0].split(' ')[2])-32)):.2f}°C",
                    self.label_humidity.cget("text"),
                    f"Pressure: {float(self.label_pressure.cget('text').split(' ')[1])*68.9476:.2f} hPa",
                    f"Visibility: {float(self.label_visibility.cget('text').split(' ')[1])*1.60934:.2f} km",
                    f"Wind Speed: {float(self.label_windspeed.cget('text').split(' ')[2])*1.60934:.2f} meters per second",
                ]
            )
            self.write_file()

    def write_file(self) -> None:
        """Write the settings to the file."""

        with open(data_file, "w") as file:
            # Clear the file
            file.truncate(0)
            file.flush()
            file.seek(0)
            file.write(f"{self.color_mode}\n{self.units}")

    def check_for_updates(self) -> None:
        # Check github for newer version

        try:
            self.api_response = requests_get(
                "https://api.github.com/repos/Futura-Py/weather/releases/latest",
                timeout=50,
            )
            self.latest_tag = self.api_response.json()["tag_name"].removeprefix("v")
        except TimeoutError:
            # Couldn't access the internet, no need to bother the user
            return

        if VERSION != self.latest_tag:
            self.doupdate = Messagebox(
                self,
                "Update available!",
                "\nDo you want to update to the newest version?\n\nYou will be redirected to our release page where you can download the newest binaries.",
                None,
                buttons=[("Yes", True, "accent"), ("No", False)],
            )
            if self.doupdate.result:
                openwebpage(self.api_response.json()["html_url"])
                self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
