import customtkinter as ctk
import json  # noqa: F401
import secrets
import string
from datetime import datetime  # noqa: F401


# App setup
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(string="Password Generator")
        self.resizable(width=False, height=False)
        ctk.set_appearance_mode(mode_string="dark")

        self._center_window()
        self._setup_ui()

    def _setup_ui(self):
        ## Paths
        def_font_pth = "fonts/Roboto-Medium.ttf"
        def_ico_pth = "icons/lock.ico"

        ## Fonts & icons setup
        ctk.FontManager.load_font(font_path=def_font_pth)
        def_font = ctk.CTkFont(
            family="Roboto-Medium",
            size=18,
        )
        self.iconbitmap(bitmap=def_ico_pth)

        ## App elements setup
        # Window
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)

        # Main frame
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="nsew",
        )
        self.main_frame.grid_rowconfigure(index=(0, 1, 2, 3), weight=1)
        self.main_frame.grid_columnconfigure(index=0, weight=1)

        # TODO: Change this on tooltip sign
        self.label = ctk.CTkLabel(
            master=self.main_frame, text="Hello", font=def_font
        )
        self.label.grid()

        self.entry = ctk.CTkEntry(
            master=self.main_frame,
            placeholder_text="New password's here...",
            font=def_font,
            width=350,
        )
        self.entry.grid()

        self.btn = ctk.CTkButton(
            master=self.main_frame,
            text="Generate Password",
            font=def_font,
            command=self.gen_passwd,
        )
        self.btn.grid()

        self.chkbx = ctk.CTkCheckBox(
            master=self.main_frame,
            text="Options",
            font=def_font,
        )
        self.chkbx.grid()

        self.slider = ctk.CTkSlider(
            master=self.main_frame,
            from_=8,
            to=30,
            number_of_steps=22,
        )
        self.slider.grid()
        self.slider.set(output_value=8)

        self.slider_value = ctk.CTkLabel(
            master=self.main_frame,
            font=def_font,
        )

    def _center_window(window, width=600, height=700):
        # Get screen dimensions
        screen_width: int = window.winfo_screenwidth()
        screen_height: int = window.winfo_screenheight()

        # Calculate x and y coordinates for the window to be centered
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        # Set the geometry
        window.geometry(geometry_string=f"{width}x{height}+{x}+{y}")

    # Define app functions
    def gen_passwd(self):
        length: int = 30
        alphabet: str = (
            string.ascii_letters + string.digits + string.punctuation
        )
        passwd: str = "".join(
            secrets.choice(seq=alphabet) for _ in range(length)
        )
        self.entry.delete(first_index=0, last_index="end")
        self.entry.insert(index=0, string=passwd)

    # def slider_test(self, value):
    #     print(f"Value of slider: {value}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
