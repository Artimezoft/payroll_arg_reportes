import datetime

from py_arg_reports.reporters.libro_sueldo_digital.tools import INDICE_TIPO_LIQUIDACIONES


def process_reg1(cuit: str, periodo: datetime.date, q_empleados: int, nro_liq: int, tipo_liq: str) -> tuple:
    """ Generacion txt de Libro Sueldos Digital
        Registro 1 Datos referenciales del envío de la liquidacion
        Args:
            cuit: str, CUIT del empleador
            periodo: datetime.date, fecha de la liquidacion
            q_empleados: int, cantidad de empleados liquidados
            nro_liq: int, numero de liquidacion
            tipo_liq: str, tipo de liquidacion ('M'=mes; 'Q'=quincena; 'S'=semanal)
        Retorna:
            (Resultado, Error, Registro1)
            - True, None, str: si todo salió bien
            - False, str, None: si falla
    """

    # Período en formato AAAAMM
    periodo_str = periodo.strftime('%Y%m')
    tipo_liq_aceptadas = INDICE_TIPO_LIQUIDACIONES.keys()

    # Validaciones
    cuit = cuit.replace('-', '')
    if len(cuit) != 11:
        return False, 'CUIT incorrecto', None

    if q_empleados < 1:
        return False, 'Cantidad de empleados incorrecta', None

    if nro_liq < 1:
        return False, 'Numero de liquidacion incorrecto', None

    if tipo_liq not in tipo_liq_aceptadas:
        return False, 'Tipo de liquidacion no aceptada', None

    tipo_liquidacion = INDICE_TIPO_LIQUIDACIONES[tipo_liq]

    # Pendiente tipo de liquidacion rectificativa
    resp = f'01{cuit}SJ'
    resp += periodo_str
    resp += tipo_liquidacion
    resp += str(nro_liq).zfill(5)

    ds_base = 30
    resp += str(ds_base).zfill(2) + str(q_empleados).zfill(6)

    return True, None, resp
