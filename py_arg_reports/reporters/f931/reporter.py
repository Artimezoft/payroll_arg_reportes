from py_arg_reports.reporters.f931.tools import FORMATO_TXT_F931
from py_arg_reports.tools.tools import sync_format


def genera_txt_f931(
    json_data: dict,
    output_path: str,
    filename: str = None,
) -> tuple:
    """ Genera el archivo de texto para la F931,
        Args:
            json_data: dict, datos de F931 Fijos
            output_path: str, ruta donde se guardará el archivo
            filename: str, nombre del archivo

        Retorna una tupla:
         - False, error: si falla
         - True, None: si todo salió bien
    """
    resp = None

    if not json_data.get('txt_empleados'):
        return False, 'No se puede generar el txt para el F931, no hay datos'

    # Configurar filename si usuario no lo especifica
    if not filename:
        filename = f'txt_f931_{json_data["cuit"]}_{json_data["periodo"]}'

    # Crear archivo vacio
    full_path = f'{output_path}/{filename}.txt'
    with open(full_path, 'w', encoding='cp1252') as f:
        f.write('')

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

            # Situaciones de Revista 2 y 3 no pueden ser vacías o "00", cambiar a "01" si es así
            if field_name in ['situacion_2', 'situacion_3'] and (info_formatted == '00' or info_formatted == '  '):
                info_formatted = '01'

            line += info_formatted
        # Agregar salto de linea
        line += '\n'
        # Escribir linea en el archivo
        with open(full_path, 'a', encoding='latin-1') as f:
            f.write(line)

    return True, resp
