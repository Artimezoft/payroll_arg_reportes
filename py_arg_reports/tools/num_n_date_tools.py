
def draw_text_with_end_coordinate(canvas, x_end, y, text, font_family='Helvetica', font_size=8):
    # Calculate the width of the text
    text_width = canvas.stringWidth(text, font_family, font_size)

    # Adjust the starting x-coordinate to place the text's end at x_end
    x_start = x_end - text_width

    # Draw the text
    canvas.drawString(x_start, y, text)


def formatted_date_str(date_str: str) -> str:
    """
    Converts a date string in the format YYYY-MM-DD to the format DD/MM/YYYY
    """
    return date_str[8:] + "/" + date_str[5:7] + "/" + date_str[:4]


def float_to_format_currency(float_value: float, include_currency: bool = True) -> str:
    """ Converts a float value to a string formatted as a currency
        I also add thousands separators and two decimal places
        decimal is separated by comma and thousands by dot
    """
    resp = "{:,.2f}".format(float_value)
    resp = resp.replace(",", "X").replace(".", ",").replace("X", ".")
    currency = "$ " if include_currency else ""

    return f'{currency}{resp}'

def nombre_mes(mes: int) -> str:
    month_names = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }
    return month_names.get(mes, "Mes inválido")
