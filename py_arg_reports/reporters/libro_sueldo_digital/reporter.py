import datetime

from py_arg_reports.reporters.libro_sueldo_digital.generador_registros import(
    registro1,
    registro2,
    registro3,
    registro4,
    registro5,
)
from py_arg_reports.reporters.libro_sueldo_digital.tools import FORMATO_TXT_LSD
from py_arg_reports.tools.tools import sync_format

""" Ejemplo de json_data en samples/lsd-info.json
"""


def genera_txt_lsd_liquidacion(
    cuit: str,
    liquidacion_data = dict,
) -> tuple:
    """ Genera el archivo de texto para la generación del Libro Sueldo Digital
        Para una liquidación en particular
        Args:
            cuit: str, CUIT del empleador
            liquidacion_data: dict, datos de liquidación

        Retorna una tupla:
         - False, error: si falla
         - True, None: si todo salió bien
    """


def genera_txt_lsd(
    json_data: dict,
    output_path: str,
    filename: str = None,
) -> tuple:
    """ Genera el archivo de texto para la generación del Libro Sueldo Digital
        Args:
            json_data: dict, datos de F931 Fijos
            output_path: str, ruta donde se guardará el archivo
            filename: str, nombre del archivo. En caso una liquidación genera txt, sino se genera un zip
            con todos los archivos de liquidaciones

        Retorna una tupla:
         - False, error: si falla
         - True, None: si todo salió bien
    """
    resp = None
    indices_esenciales = ['periodo', 'cuit', 'cantidad_liquidaciones', 'liquidaciones']
    indices_esenciales_liquidaciones = ['tipo_liquidacion', 'fecha_pago', 'empleados_liquidados']

    # Validar que json_data tenga los datos esenciales
    for indice in indices_esenciales:
        if not json_data.get(indice):
            return False, f'No se puede generar el txt, dato esencial {indice} no encontrado'

    # Tomo las variables esenciales
    cuit = json_data['cuit']
    periodo = json_data['periodo']
    periodo_date = datetime.datetime.strptime(periodo, '%Y-%m-%d').date()
    liquidaciones = json_data['liquidaciones']

    # Valido Liquidaciones
    # 1) Que sea una lista de diccionarios
    # 2) Que tenga los datos esenciales
    if not isinstance(liquidaciones, list):
        return False, 'No se puede generar el txt, liquidaciones no es una lista de diccionarios'

    for liquidacion in liquidaciones:
        if not isinstance(liquidacion, dict):
            return False, 'No se puede generar el txt, liquidaciones no es una lista de diccionarios'

        for indice in indices_esenciales_liquidaciones:
            if not liquidacion.get(indice):
                return False, f'No se puede generar el txt, dato esencial {indice} no encontrado en liquidaciones'

    # Configurar filename si usuario no lo especifica
    if not filename:
        filename = f'txt_lsd_{cuit}_{periodo}'

    # Comienzo dato por dato de json_data a generar en el txt linea por linea
    for empleado in json_data['txt_empleados']:
        # Generar linea por empleado
        line = ''
        for field_name in FORMATO_TXT_F931:
            if field_name not in empleado.keys():
                return False, f'El campo {field_name} no fue encontrado en los datos'
            tipo_dato = FORMATO_TXT_F931[field_name]['type']
            if tipo_dato == 'DE':
                multiplicador = FORMATO_TXT_F931[field_name].get('multiplicador', 100)
            else:
                multiplicador = FORMATO_TXT_F931[field_name].get('multiplicador', 1)
            largo = FORMATO_TXT_F931[field_name]['long']
            info = empleado[field_name]
            info_formatted = sync_format(str(info), largo, tipo_dato, multiplicador)
            line += info_formatted
        # Agregar salto de linea
        line += '\n'
        # Escribir linea en el archivo
        with open(full_path, 'a') as f:
            f.write(line)

    # Crear archivo vacio
    full_path = f'{output_path}/{filename}.txt'
    with open(full_path, 'w') as f:
        f.write('')

    return True, resp
