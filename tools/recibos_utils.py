
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

    return f'{currency} {resp}'


def draw_text_with_max_width(canvas, text, max_width, x, y):
    formatted_text = textObject(canvas, text, max_width, x, y)

    canvas.drawText(formatted_text)


def textObject(canvas, text, max_width, x, y):
    # Create a text object with the specified max width
    text_object = canvas.beginText(0, 0)
    text_object.setTextOrigin(x, y)
    canvas_font = canvas._fontname
    canvas_font_size = canvas._fontsize
    text_object.setFont(canvas_font, canvas_font_size)

    words = text.split()
    current_line = []
    current_line_width = 0

    for word in words:
        word_width = canvas.stringWidth(word + " ", canvas_font, canvas_font_size)
        if current_line_width + word_width <= max_width:
            current_line.append(word)
            current_line_width += word_width
        else:
            text_object.textLine(" ".join(current_line))
            current_line = [word]
            current_line_width = word_width

    if current_line:
        text_object.textLine(" ".join(current_line))

    return text_object


def nombre_mes(mes: int) -> str:
    if mes == 1:
        return "Enero"
    elif mes == 2:
        return "Febrero"
    elif mes == 3:
        return "Marzo"
    elif mes == 4:
        return "Abril"
    elif mes == 5:
        return "Mayo"
    elif mes == 6:
        return "Junio"
    elif mes == 7:
        return "Julio"
    elif mes == 8:
        return "Agosto"
    elif mes == 9:
        return "Septiembre"
    elif mes == 10:
        return "Octubre"
    elif mes == 11:
        return "Noviembre"
    elif mes == 12:
        return "Diciembre"
