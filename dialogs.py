from functools import partial
from sys import platform
from tkinter import Toplevel, TclError
from tkinter.ttk import Frame, Label, Button

class Messagebox(Toplevel):
    def __init__(self, parent, title, details, icon, *, buttons) -> bool:
        super().__init__()
        
        self.result = None

        self.big_frame = Frame(self)
        self.big_frame.pack(fill="both", expand=True)
        self.big_frame.columnconfigure(0, weight=1)
        self.big_frame.rowconfigure(0, weight=1)

        info_frame = Frame(self.big_frame, padding=(10, 12), style="Dialog_info.TFrame")
        info_frame.grid(row=0, column=0, sticky="nsew")
        info_frame.columnconfigure(1, weight=1)
        info_frame.rowconfigure(1, weight=1)

        try: self.color = self.big_frame.tk.call("set", "themeColors::dialogInfoBg")
        except TclError: self.color = self.big_frame.tk.call("ttk::style", "lookup", "TFrame", "-background")

        self.icon_label = Label(info_frame, image=icon, anchor="nw", background=self.color)
        if icon is not None: self.icon_label.grid(row=0, column=0, sticky="nsew", padx=(12, 0), pady=10, rowspan=2)

        self.title_label = Label(info_frame, text=title, anchor="nw", font=("", 14, "bold"), background=self.color)
        self.title_label.grid(row=0, column=1, sticky="nsew", padx=(12, 17), pady=(10, 8))

        self.detail_label = Label(info_frame, text=details, anchor="nw", background=self.color)
        self.detail_label.grid(row=1, column=1, sticky="nsew", padx=(12, 17), pady=(5, 10))

        self.button_frame = Frame(self.big_frame, padding=(22, 22, 12, 22), style="Dialog_buttons.TFrame")
        self.button_frame.grid(row=2, column=0, sticky="nsew")

        for index, button_value in enumerate(buttons):
            self.style = None
            self.state = None
            self.default = False
            self.sticky = "nes" if len(buttons) == 1 else "nsew"

            if len(button_value) > 2:
                if button_value[2] == "accent":
                    self.style = "Accent.TButton"
                    self.default = True
                elif button_value[2] == "disabled":
                    self.state = "disabled"
                elif button_value[2] == "default":
                    self.default = True

            self.button = Button(self.button_frame, text=button_value[0], width=18, command=partial(self.on_button, button_value[1]), style=self.style, state=self.state)
            if self.default:
                self.button.bind("<Return>", self.button["command"])
                self.button.focus()

            self.button.grid(row=0, column=index, sticky=self.sticky, padx=(0, 10))

            self.button_frame.columnconfigure(index, weight=1)

        self.update_idletasks()

        self.dialog_width = self.winfo_width()
        self.dialog_height = self.winfo_height()

        if parent is None:
            self.parent_width = self.winfo_screenwidth()
            self.parent_height = self.winfo_screenheight()
            self.parent_x = 0
            self.parent_y = 0
        else:
            self.parent_width = parent.winfo_width()
            self.parent_height = parent.winfo_height()
            self.parent_x = parent.winfo_x()
            self.parent_y = parent.winfo_y()

        self.x_coord = int(self.parent_width / 2 + self.parent_x - self.dialog_width / 2)
        self.y_coord = int(self.parent_height / 2 + self.parent_y - self.dialog_height / 2)

        self.geometry("+{}+{}".format(self.x_coord, self.y_coord))
        self.minsize(320, self.dialog_height)

        self.transient(parent)

        if platform != 'win32':
            self.wm_attributes("-type", "dialog")
            
        self.grab_set()

        self.wait_window()

    def on_button(self, value):
        self.result = value
        self.destroy()