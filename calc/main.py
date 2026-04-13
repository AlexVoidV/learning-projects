import dearpygui.dearpygui as dpg
import math
# import decimal
# import re
# import typing


# Reference: Windows Calculator.

buttons: list[list[str]] = [
    ["%", "C", "<x"],
    ["1/x", "x^2", "2sqrtx", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["+/-", "0", ",", "="],
]

digitals_list: list[str] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
operands_list: list[str] = ["+", "-", "*", "/"]

# TODO: typehints
# TODO: docstrings
# TODO: langs dictionary
# TODO: setup theme?
# TODO: tests
# TODO: exceptions

# The entered digit or number
current_input: str = ""
# To save the first number (based on the current input)
first_num: str = ""
operation: str = ""


# TODO: callbacks will be here
def on_button_pressed(sender, app_data, user_data: str):
    global current_input, first_num, operation
    print(f"Button Data: {user_data}")
    button_data: str = user_data

    if button_data in digitals_list:
        current_input += button_data

        if current_input == "0":
            pass  # idk

        print(f"{current_input} - memorized the number!")
        update_display()  # Number output
        print("The num: entered, now output in second line text!")

    if button_data in operands_list:
        if current_input:
            first_num = current_input
            operation = button_data
            update_calculations(first_num, operation)
            current_input = ""

    # maybe delete this
    match button_data:
        case "C":
            pass
        case "<x":
            pass
        case "%":
            pass
        case "1/x":
            pass
        case "x^2":
            pass
        case "2sqrtx":
            pass
        case "+/-":
            pass
        case "=":
            pass


def update_display():
    """Updates the text on the second line (with the "display" tag).
    This can be an input number, as well as a result."""
    global current_input
    dpg.set_value("display", current_input)
    # it should display the entered number or the result of the operation.


def update_calculations(first_num: str, operation: str):
    """Shows the first number entered and the operator,
    but only when the operator is selected.
    Then adds '='.
    Does not show the result.
    It is updated on a new operation (remembers the amount).

    Args:
        first_num (str): The first number entered.
        operation (str): Operator.
    """
    print("Output calculations to the first line")
    # The counting line (operations)
    all_in_one: str = first_num + operation
    print(f"All together - {all_in_one}")
    dpg.set_value("calculations", all_in_one)


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
        dpg.add_text(
            default_value="",
            tag="calculations",
        )
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
                    dpg.add_button(
                        label=btn,
                        width=btn_width,
                        callback=on_button_pressed,
                        user_data=btn,
                    )
                    # add callbacks for operation buttons

    dpg.create_viewport(title="Calculator App", width=450, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
