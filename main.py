from __future__ import annotations

from platform import system
from tkinter import Menu, Tk, messagebox
from tkinter.ttk import Button, Entry, Frame, Label, Style

import requests

SYSTEM = str(system())

# NOTE: Before making any commits, please run the following command:
# black .; isort .; ruff . --fix

def self_return_decorator(func, *args, **kwargs):
    # Allows for chaining of methods
    # Example:
    # App.OWMCITY().method1().method2()
    # This does assume however that the methods don't have any return values
    # If they do, then the return value will not be returned
    # This is because the return value is the App object, not the return value of the method
    def self_returner(self=None, *args, **kwargs):
        func(self, *args, **kwargs)
        return self

    return self_returner


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

        Style().theme_use("clam")

        # Set up window
        self.title("Weather")
        self.resizable(False, False)
        self.configure(bg="white")

        # Set up widgets
        self.main_frame = Frame(self, padding=10)
        self.main_frame.pack()

        heading = Label(self.main_frame, text="Weather", font="Helvetica 13")
        heading.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.searchbar = Entry(self.main_frame, width=42)
        self.searchbar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.label = Label(self.main_frame, text="", font=("Helvetica 13"))
        self.label.grid(row=2, column=0, columnspan=2)

        Button(self.main_frame, text="Search for City", command=self.OWMCITY).grid(
            row=3, column=0, padx=10, pady=10
        )
        Button(self.main_frame, text="Exit", command=self.exit_app).grid(
            row=3, column=1, padx=10, pady=10
        )

        self.resize_app()
        self.deiconify()

    @self_return_decorator
    def about(self) -> App:
        """Display a messagebox with information about the app."""
        messagebox.showinfo(
            "About Weather",
            "Weather is a simple weather app that uses the OpenWeatherMap API to get the weather for a given city.",
            parent=self,
        )

    @self_return_decorator
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
        self.geometry(f"{minimum_width}x{minimum_height}+{x_coords}+{y_coords}")
        self.wm_minsize(minimum_width, minimum_height)

    def exit_app(self) -> None:
        """Exit the app."""
        self.destroy()

    @self_return_decorator
    def OWMCITY(self) -> App:
        # Get API key
        api_key = "c439e1209216cc7e7c73a3a8d1d12bfd"

        # Get city name
        city = self.searchbar.get()

        # Send request to OpenWeatherMap API
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        )
        if response.status_code != 200:
            self.label.configure(text="City not found")
            return

        # Get temperature in Celsius
        temperature_kelvin = response.json()["main"]["temp"]
        temperature_celsius = temperature_kelvin - 273.15

        # Put in label
        self.label.configure(text=f"{temperature_celsius:.2f}°C")


if __name__ == "__main__":
    app = App()
    app.mainloop()
