def integer_to_amount_txt(amount: int, long: int, multiplicador: int = 1) -> str:
    """ Convierte un monto entero a formato de texto
    """
    resp = amount * multiplicador
    resp = str(resp).zfill(long)
    return resp


def float_to_amount_txt(amount: float, long: int, multiplicador: int = 100) -> str:
    """ Convierte un monto float a formato de texto
    """
    resp = "{:.2f}".format(amount)
    resp = resp.zfill(long).replace('.', ',')
    return resp


def amount_txt_to_integer(amount_txt: str, mulitp=100) -> int:
    """ Convierte un monto en formato de texto a entero
    """
    resp = float(amount_txt.replace(',', '.')) * mulitp
    resp = int(resp)

    return resp


def amount_txt_to_float(amount_txt: str, multip: int = 100, rount_to: int = 2) -> float:
    """ Convierte un monto en formato de texto a float
    """
    resp = float(amount_txt.replace(',', '.')) * multip
    resp = float(resp)
    resp = round(resp, rount_to)

    return resp


def sync_format(info: str, expected_len: int, type_info: str, multiplicador: int = 1) -> str:
    """ Sincroniza el formato de un campo de un txt de F931
        Args:
            info: str, valor del campo
            expected_len: int, longitud esperada del campo
            type_info: str, tipo de campo, estos pueden ser:
                EN - Entero
                DE - Decimal
                AL - Alfabético
                AN - Alfanumérico
                BO - Booleano
            multiplicador: int, multiplicador del campo
    """
    resp = info
    if type_info == 'BO':
        resp = '1' if info else '0'
        return resp

    if len(info) != expected_len or ',' in info:
        if len(info) > expected_len and not type_info == 'BO':
            resp = round(float(info.replace(',', '.').strip()))
            # Ver si está ok multiplicar por 100
            resp = str(resp * multiplicador).zfill(expected_len)
        else:
            if type_info == 'DE':
                resp = float_to_amount_txt(float(info), expected_len, multiplicador)
            elif type_info == 'EN':
                resp = integer_to_amount_txt(int(info), expected_len, multiplicador)

    # En los otros casos (AL o AN) se completa con espacios a la derecha
    if type_info in ['AL', 'AN']:
        resp = str(resp).ljust(expected_len)

    return resp


def convert_to_float_if_possible(value_str: str):
    """Convert the value_str to float if possible, else return the value_str
    """
    try:
        return float(value_str)
    except ValueError:
        return value_str


def convert_to_int_if_possible(value_str: str):
    """Convert the value_str to int if possible, else return the value_str
    """
    try:
        return int(value_str)
    except ValueError:
        return value_str
