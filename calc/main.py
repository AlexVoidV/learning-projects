import dearpygui.dearpygui as dpg
import math


buttons: list[list[str]] = [
    ["%", "C", "<x"],
    ["1/x", "x^2", "2sqrtx", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["+/-", "0", ",", "="],
]


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    return a / b


def mod(a, b):
    return a % b


def per(a):
    return a / 100


def inv(a):
    return 1 / a


def sqr(a):
    return a**2


def sqrt(a):
    return math.sqrt(a)


def main():
    dpg.create_context()

    # Setup font
    with dpg.font_registry():
        default_font: int | str = dpg.add_font("font/Roboto-Medium.ttf", 20)

    dpg.bind_font(default_font)

    # App window
    with dpg.window(tag="Primary Window"):
        dpg.add_input_text(
            tag="display",
            width=-1,
            height=30,
            readonly=True,
            default_value="0",
        )

        for row in buttons:
            with dpg.group(horizontal=True):
                for btn in row:
                    btn_width = 70
                    dpg.add_button(label=btn, width=btn_width)

    dpg.create_viewport(title="Calculator App", width=450, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
