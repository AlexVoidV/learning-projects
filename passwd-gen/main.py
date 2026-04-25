from typing import Literal
import customtkinter as ctk
import secrets
import string  # Soon will be deleted


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
        self.main_frame.grid_rowconfigure(index=(0, 1, 2, 3, 4), weight=1)
        self.main_frame.grid_columnconfigure(index=(0, 1, 2), weight=1)

        # Entry field for password
        self.entry = ctk.CTkEntry(
            master=self.main_frame,
            placeholder_text="New password's here...",
            font=def_font,
            width=400,
        )
        self.entry.grid()

        # Generate password button
        self.btn = ctk.CTkButton(
            master=self.main_frame,
            text="Generate Password",
            font=def_font,
            command=self.gen_passwd,
        )
        self.btn.grid()

        # Second frame for checkboxes
        self.cbx_frame = ctk.CTkFrame(
            master=self.main_frame,
        )
        self.cbx_frame.grid()

        ## Options with checkboxes
        # Variables
        self.upper_var = ctk.BooleanVar(value=True)
        self.lower_var = ctk.BooleanVar(value=True)
        self.digits_var = ctk.BooleanVar(value=True)
        self.symbols_var = ctk.BooleanVar(value=True)

        # Checkboxes
        self.cbx_up_case = ctk.CTkCheckBox(
            master=self.cbx_frame,
            text="A-Z",
            font=def_font,
            variable=self.upper_var,
        )
        self.cbx_up_case.grid()

        self.cbx_lw_case = ctk.CTkCheckBox(
            master=self.cbx_frame,
            text="a-z",
            font=def_font,
            variable=self.lower_var,
        )
        self.cbx_lw_case.grid()

        self.cbx_digits = ctk.CTkCheckBox(
            master=self.cbx_frame,
            text="0-9",
            font=def_font,
            variable=self.digits_var,
        )
        self.cbx_digits.grid()

        self.cbx_symbols = ctk.CTkCheckBox(
            master=self.cbx_frame,
            text="!@#$%^&*_-",
            font=def_font,
            variable=self.symbols_var,
        )
        self.cbx_symbols.grid()

        # Slider for length of password
        self.slider = ctk.CTkSlider(
            master=self.main_frame,
            from_=8,
            to=30,
            number_of_steps=22,
            command=self.upd_slider_info,
        )
        self.slider.grid()
        self.slider.set(output_value=8)

        # Label with slider's value
        self.slider_label = ctk.CTkLabel(
            master=self.main_frame,
            font=def_font,
            text=f"Length: {int(float(self.slider.get()))}",
        )
        self.slider_label.grid()

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
        # Define variables
        length: int = int(float(self.slider.get()))

        letters_lw: Literal["abcdefghijklmnopqrstuvwxyz"] = (
            string.ascii_lowercase
        )
        letters_up: Literal["ABCDEFGHIJKLMNOPQRSTUVWXYZ"] = (
            string.ascii_uppercase
        )
        digits: Literal["0123456789"] = string.digits
        symbols: Literal["!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"] = (
            string.punctuation
        )

        # The minimum password includes
        passwd: list[str] = [
            secrets.choice(seq=letters_lw),
            secrets.choice(seq=letters_up),
            secrets.choice(seq=digits),
            secrets.choice(seq=symbols),
        ]

        all_chars: Literal[
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
        ] = letters_lw + letters_up + digits + symbols

        # Generate password
        passwd += [secrets.choice(seq=all_chars) for _ in range(length)]

        # Random the list
        secrets.SystemRandom().shuffle(x=passwd)

        # Delete the spaces
        password: str = "".join(passwd)

        # "Return" string
        self.entry.delete(first_index=0, last_index="end")
        self.entry.insert(index=0, string=password)

    def upd_slider_info(self, value):
        self.slider_label.configure(text=f"Length: {int(float(value))}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
