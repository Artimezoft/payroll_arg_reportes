
from py_arg_reports.reporters.libro_sueldo_digital.tools import FORMATO_TXT_LSD
from py_arg_reports.tools.tools import sync_format


KEYS_CALCULOS_ESPECIFICOS = [
    'base_calculo_diferencial_aporte_os',
    'base_calculo_diferencial_aporte_ss',
    'base_calculo_diferencial_contribucion_os',
    'base_calculo_diferencial_contribucion_ss',
    'base_calculo_diferencial_lrt',
]


def process_keys_especificas(key_sp: str, info_931: dict) -> str:
    """ Procesa las claves específicas de los cálculos de la liquidación
        Para casos particulares que no vienen en Info F.931
    """
    resp = ''
    if key_sp == 'base_calculo_diferencial_aporte_os':
        # El cálculo surge de Remuneracion4 - Remuneracion2
        remuneracion4 = info_931['remuneracion_04']
        remuneracion2 = info_931['remuneracion_02']
        resp = str(remuneracion4 - remuneracion2)
    elif key_sp == 'base_calculo_diferencial_contribucion_os':
        # El cálculo surge de Remuneracion8 - Remuneracion2
        remuneracion8 = info_931['remuneracion_08']
        remuneracion2 = info_931['remuneracion_02']
        resp = str(remuneracion8 - remuneracion2)
    else:
        # Todos los demás casos devuelven 0
        resp = "0"

    return resp


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
            # Procesa las claves específicas
            if dato in KEYS_CALCULOS_ESPECIFICOS:
                dato_value = process_keys_especificas(dato, info_931)
            else:
                # Todos los demás items deben estar en info_931
                if dato not in info_931:
                    return False, f'Falta el campo {dato} en el diccionario de info_931', None
                long = formato['long']
                dato_type = formato['type']
                dato_value = str(info_931[dato])
            dato_to_add = sync_format(dato_value, long, dato_type)
            resp += dato_to_add

    return True, None, resp
