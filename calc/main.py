import dearpygui.dearpygui as dpg
import math


# Reference: Windows Calculator.

icon_path = "icon/calculator.ico"

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

# The currently entered digit or number (default = "0")
current_input: str = "0"
# The first operand (stored when an operator is pressed)
first_num: str = ""
# The current operation (+, -, *, /)
operation: str = ""
# Flag: was the '=' button pressed last time
is_eq_pressed: bool = False
# The second operand (stored for repeated '=' presses)
last_operand: str = ""


def on_button_pressed(sender, app_data, user_data: str):
    global current_input, first_num, operation, is_eq_pressed, last_operand
    button_data: str = user_data

    # Digits (0-9)
    if button_data in digitals_list:
        if current_input == "0" or is_eq_pressed:
            current_input = button_data
            is_eq_pressed = False
        else:
            current_input += button_data
        update_display()

    # Operators (+, -, *, /)
    elif button_data in operands_list:
        if is_eq_pressed:
            # After '=' press: start new operation with current result
            first_num = current_input
            current_input = ""
            is_eq_pressed = False
            last_operand = ""
        elif first_num and operation and current_input:
            # Chained operation: compute intermediate result
            result = calculate(
                float(first_num), float(current_input), operation
            )
            first_num = str(result)
            current_input = ""
        elif current_input:
            # First operator: store the number
            first_num = current_input
            current_input = ""
        operation = button_data
        update_calculations(first_num, operation, show_eq=False)

    # Decimal point
    elif button_data == ",":
        if is_eq_pressed:
            current_input = "0."
            is_eq_pressed = False
        elif "." not in current_input:
            current_input += "."
        update_display()

    # Equals button
    elif button_data == "=":
        if is_eq_pressed and operation and last_operand:
            # Repeated '=' press: apply operation with the stored second operand
            result = calculate(
                float(current_input), float(last_operand), operation
            )
            update_calculations(
                current_input, operation, last_operand, show_eq=True
            )
            current_input = str(result)
            update_display()
        elif first_num and operation and current_input:
            # First '=' press: store the second operand for repetition
            is_eq_pressed = True
            last_operand = current_input
            result = calculate(
                float(first_num), float(current_input), operation
            )
            update_calculations(
                first_num, operation, current_input, show_eq=True
            )
            first_num = str(result)
            current_input = str(result)
            update_display()

    # Clear button
    elif button_data == "C":
        current_input = "0"
        first_num = ""
        operation = ""
        is_eq_pressed = False
        last_operand = ""
        dpg.set_value("calculations", "")
        update_display()

    # Backspace button
    elif button_data == "<x":
        if current_input and current_input != "0":
            current_input = current_input[:-1]
            if current_input == "" or current_input == "-":
                current_input = "0"
            update_display()

    # Percentage button
    elif button_data == "%":
        if current_input:
            try:
                current_input = str(per(float(current_input)))
                update_display()
            except ValueError, OverflowError:
                current_input = "Error"
                update_display()

    # Inverse button
    elif button_data == "1/x":
        if current_input:
            try:
                val = float(current_input)
                if val == 0:
                    current_input = "Error"
                else:
                    current_input = str(inv(val))
                update_display()
            except ValueError, OverflowError:
                current_input = "Error"
                update_display()

    # Square button
    elif button_data == "x^2":
        if current_input:
            try:
                current_input = str(sqr(float(current_input)))
                update_display()
            except ValueError, OverflowError:
                current_input = "Error"
                update_display()

    # Square root button
    elif button_data == "2sqrtx":
        if current_input:
            try:
                val = float(current_input)
                if val < 0:
                    current_input = "Error"
                else:
                    current_input = str(sqrt(val))
                update_display()
            except ValueError, OverflowError:
                current_input = "Error"
                update_display()

    # Sign change button
    elif button_data == "+/-":
        if current_input and current_input != "0":
            if current_input.startswith("-"):
                current_input = current_input[1:]
            else:
                current_input = "-" + current_input
            update_display()


def calculate(a: float, b: float, op: str) -> str:
    """Computes the result and returns a rounded string."""
    try:
        match op:
            case "+":
                result = add(a, b)
            case "-":
                result = sub(a, b)
            case "*":
                result = mul(a, b)
            case "/":
                if b == 0:
                    return "Error"
                result = div(a, b)

        # Check for infinity or NaN
        if math.isinf(result) or math.isnan(result):
            return "Error"

        # Round to 10 decimal places to avoid float precision issues
        # :g removes the trailing .0 for integers, but retains the fractional part
        return f"{round(result, 10):.12g}"
    except OverflowError:
        return "Error"


def update_display():
    """Updates the text on the second line (with the 'display' tag).
    This can be an input number or a result."""
    dpg.set_value("display", current_input)


def update_calculations(
    first_num: str, operation: str, second_num: str = "", show_eq: bool = False
):
    """Updates the first line showing the calculation expression.

    Args:
        first_num: The first operand.
        operation: The operator (+, -, *, /).
        second_num: The second operand (shown when show_eq=True).
        show_eq: If True, shows the full expression with '=' (e.g., '5 + 3 =').
                 If False, shows just the expression (e.g., '5 +').
    """
    if show_eq:
        all_in_one = f"{first_num} {operation} {second_num} ="
    elif operation:
        all_in_one = f"{first_num} {operation}"
    else:
        all_in_one = ""
    dpg.set_value("calculations", all_in_one)


def add(a: float, b: float) -> float:
    return a + b


def sub(a: float, b: float) -> float:
    return a - b


def mul(a: float, b: float) -> float:
    return a * b


def div(a: float, b: float) -> float:
    return a / b


def per(a: float) -> float:
    return a / 100


def inv(a: float) -> float:
    if a == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return 1 / a


def sqr(a: float) -> float:
    result = a**2
    if math.isinf(result):
        raise OverflowError("Result is too large")
    return result


def sqrt(a: float) -> float:
    if a < 0:
        raise ValueError("Cannot calculate square root of a negative number")
    return math.sqrt(a)


def main():
    dpg.create_context()

    # Setup font
    with dpg.font_registry():
        default_font: int | str = dpg.add_font("font/Roboto-Medium.ttf", 20)

    dpg.bind_font(default_font)

    # App window
    with dpg.window(tag="Primary Window"):
        # Style for text displays (remove borders)
        with dpg.theme() as no_border_theme:
            with dpg.theme_component(dpg.mvInputText):
                dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (0, 0, 0, 0))

        # Larger font for displays
        with dpg.font_registry():
            large_font = dpg.add_font("font/Roboto-Medium.ttf", 28)

        # Calculations display (top line)
        dpg.add_text(
            default_value="",
            tag="calculations",
        )

        # Main display with larger font and no border
        dpg.add_input_text(
            tag="display",
            width=-1,
            readonly=True,
            default_value="0",
        )
        dpg.bind_item_theme("display", no_border_theme)
        dpg.bind_item_font("display", large_font)
        dpg.bind_item_font("calculations", large_font)

        # Add vertical spacing to push buttons to the bottom
        dpg.add_spacer(height=40)

        # Style for buttons
        with dpg.theme() as button_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 5, 5)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 10)

        with dpg.table(
            header_row=False,
            resizable=False,
            policy=dpg.mvTable_SizingStretchProp,
        ):
            for i in range(4):
                dpg.add_table_column(init_width_or_weight=1.0)

            for row in buttons:
                with dpg.table_row():
                    for btn in row:
                        with dpg.table_cell():
                            dpg.add_button(
                                label=btn,
                                width=-1,
                                height=55,
                                callback=on_button_pressed,
                                user_data=btn,
                            )
                            dpg.bind_item_theme(dpg.last_item(), button_theme)

    dpg.create_viewport(
        title="Calculator App",
        width=350,
        height=550,
        resizable=False,
        small_icon=icon_path,
        large_icon=icon_path,
    )
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
