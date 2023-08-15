from __future__ import annotations

from platform import system
from tkinter import Event, Menu, Tk, Toplevel, messagebox
from tkinter.ttk import Button, Entry, Frame, Label, Progressbar, Style

from pyowm import OWM
from pyowm.commons.exceptions import APIRequestError
from pyowm.commons.exceptions import NotFoundError as OWMNotFoundError
from requests import Response
from requests import get as requests_get


class ProgressBar(Toplevel):
    def __init__(self, *args, **kwargs):
        # Set up window
        Toplevel.__init__(self, *args, **kwargs)
        self.withdraw()
        self.title("Loading...")
        self.resizable(False, False)

        # Set up widgets
        self.main_frame = Frame(self)
        self.main_frame.grid()

        main_label = Label(self.main_frame, text="Loading...", font="Helvetica 15 bold")
        main_label.grid(padx=10, pady=10)

        self.progressbar = Progressbar(
            self.main_frame,
            orient="horizontal",
            length=200,
            mode="indeterminate",
            maximum=4,
        )
        self.progressbar.grid(padx=10, pady=10)

        self.resize_app()
        self.update_idletasks()
        self.after_idle(lambda: self.deiconify())

    def resize_app(self) -> None:
        """Use tkinter to detect the minimum size of the app, get the center of the screen, and place the app there."""

        # TODO: Make a global function for this to remove boilerplate code
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

    def set_progress(self, progress: int):
        self.progressbar.step(progress)


class App(Tk):
    def __init__(self):
        super().__init__()
        self.bind("<Return>", self.OWMCITY)
        self.deiconify()

    def OWMCITY(self, _: Event | None = None) -> None:
        """Get the weather for a given city using the OpenWeatherMap API and display it in a label."""

        pb = ProgressBar()
        # pb.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
