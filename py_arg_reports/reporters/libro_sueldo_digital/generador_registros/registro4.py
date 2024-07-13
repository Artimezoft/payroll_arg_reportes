
from py_arg_reports.reporters.libro_sueldo_digital.tools import FORMATO_TXT_LSD
from py_arg_reports.tools.tools import sync_format


def process_reg4(cuil: str, info_931: dict) -> tuple:
    """ Generacion txt de Libro Sueldos Digital
        Registro 4 Datos referenciales de la Liquidación de SyJ del trabajador
        Args:
            cuil: str, CUIL del trabajador
            info_931: dict, datos de la liquidación
            Retorna:
            (Resultado, Error, Registro4)
            - True, None, str: si todo salió bien
            - False, str, None: si falla
    """
    resp = ''
    formato_txt_r4 = FORMATO_TXT_LSD['registro4']

    if len(cuil) != 11:
        return False, 'CUIL inválido', None

    for dato, formato in formato_txt_r4.items():
        if dato == 'tipo_registro':
            resp += '04'
        elif dato == 'cuil':
            resp += cuil
        else:
            # Todos los demás items deben estar en info_931
            if dato not in info_931:
                return False, f'Falta el campo {dato} en el diccionario de info_931', None
            long = formato['long']
            dato_type = formato['type']
            dato_value = info_931[dato]
            dato_to_add = sync_format(dato_value, long, dato_type)
            resp += dato_to_add

    return True, None, resp
