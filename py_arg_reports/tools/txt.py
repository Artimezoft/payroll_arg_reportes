def fixed_width_str(text, width, align='left', fill_with=' '):
    """
    Returns a string with fixed width. If the text is longer than the width, it will be truncated.
    """
    if len(text) > width:
        return text[:width]
    if align == 'left':
        return text + fill_with * (width - len(text))
    elif align == 'right':
        return fill_with * (width - len(text)) + text
    else:
        raise ValueError(f'Invalid align value: {align}')


def str_dec_num_to_no_dec_sep(str_num):
    """ Tengo un numero como string en un JSON y necesito sus partes entera y decimal """
    importe = float(str_num)
    parte_entera = int(importe)
    parte_decimal = int((importe - parte_entera) * 100)
    return parte_entera, parte_decimal


if __name__ == '__main__':
    assert fixed_width_str('Hello', 10) == 'Hello     '
    assert fixed_width_str('Hello', 10, align='right') == '     Hello'
    assert fixed_width_str('174', 7, fill_with='0') == '1740000'
    assert fixed_width_str('174', 7, fill_with='0', align='right') == '0000174'
    assert fixed_width_str('Hello', 5, align='right') == 'Hello'
    assert fixed_width_str('Hello', 3, fill_with='*') == 'Hel'
    assert fixed_width_str('Hello', 3, align='right', fill_with='*') == 'Hel'
