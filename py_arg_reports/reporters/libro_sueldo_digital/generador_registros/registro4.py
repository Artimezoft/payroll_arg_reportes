
from py_arg_reports.reporters.libro_sueldo_digital.tools import FORMATO_TXT_LSD
from py_arg_reports.tools.tools import sync_format


KEYS_CALCULOS_ESPECIFICOS = [
    'base_calculo_diferencial_aporte_ss',
    'base_calculo_diferencial_contribucion_ss',
    'base_calculo_diferencial_lrt',
]


def process_keys_especificas(key_sp: str, info_931: dict) -> str:
    """ Procesa las claves específicas de los cálculos de la liquidación
        Para casos particulares que no vienen en Info F.931
    """
    # Por el momento no cambia ninguno, se usaba para base diferencial de AOS y COS
    # Pero finalmente se reporta en el campo correspondiente

    resp = 0

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
        long = formato['long']
        dato_type = formato['type']
        if dato == 'tipo_registro':
            dato_to_add = '04'
        elif dato == 'cuil':
            dato_to_add = cuil
        else:
            # Procesa las claves específicas
            if dato in KEYS_CALCULOS_ESPECIFICOS:
                dato_value = process_keys_especificas(dato, info_931)
            else:
                # Todos los demás items deben estar en info_931
                if dato not in info_931:
                    return False, f'Falta el campo {dato} en el diccionario de info_931', None
                dato_value = str(info_931[dato])
                # En el caso de decimal, se multiplica por 100 porque va sin coma
                multiplicador = 100 if dato_type == 'DE' else 1
                no_coma = True if dato_type == 'DE' else False
            dato_to_add = sync_format(dato_value, long, dato_type, multiplicador, no_coma)
        resp += dato_to_add

        if len(dato_to_add) != long:
            return False, f'Error en el largo del dato {dato}', None

    return True, None, resp
