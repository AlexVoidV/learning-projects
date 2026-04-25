import customtkinter as ctk
import json  # noqa: F401
import secrets
import string
from datetime import datetime  # noqa: F401


# App setup
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Generator")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")

        self._center_window()
        self._setup_ui()

    def _setup_ui(self):
        # Variables
        def_font_pth = "fonts/Roboto-Medium.ttf"
        def_ico_pth = "icons/lock.ico"

        # Fonts & icons setup
        ctk.FontManager.load_font(def_font_pth)
        def_font = ctk.CTkFont(
            family="Roboto-Medium",
            size=18,
        )
        self.iconbitmap(def_ico_pth)

        # App elements setup
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack()

        self.label = ctk.CTkLabel(self.main_frame, text="Hello", font=def_font)
        self.label.pack()

        self.entry = ctk.CTkEntry(
            self.main_frame, placeholder_text="New password's here..."
        )
        self.entry.pack()

        self.btn = ctk.CTkButton(
            self.main_frame,
            text="Generate Password",
            font=def_font,
            command=self.gen_passwd,
        )
        self.btn.pack()

        self.chkbx = ctk.CTkCheckBox(self.main_frame, text="Options")
        self.chkbx.pack()

        self.slider = ctk.CTkSlider(
            self.main_frame,
            from_=8,
            to=30,
            number_of_steps=22,
        )
        self.slider.pack()
        self.slider.set(8)

    def _center_window(window, width=600, height=700):
        # Get screen dimensions
        screen_width: int = window.winfo_screenwidth()
        screen_height: int = window.winfo_screenheight()

        # Calculate x and y coordinates for the window to be centered
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        # Set the geometry
        window.geometry(f"{width}x{height}+{x}+{y}")

    # Define app functions
    def gen_passwd(self):
        length: int = 18
        alphabet: str = (
            string.ascii_letters + string.digits + string.punctuation
        )
        passwd: str = "".join(secrets.choice(alphabet) for _ in range(length))
        self.entry.delete(0, "end")
        self.entry.insert(0, passwd)

    # def slider_test(self, value):
    #     print(f"Value of slider: {value}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
