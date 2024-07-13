import datetime

from py_arg_reports.reporters.libro_sueldo_digital.generador_registros import (
    process_reg1,
    process_reg2,
    process_reg3,
    process_reg4,
    process_reg5,
)
from py_arg_reports.tools.tools import sync_format


def genera_txt_lsd_liquidacion(
    cuit: str,
    periodo: datetime.date,
    liquidacion_data: dict,
    nro_liq: int,
) -> tuple:
    """ Genera el archivo de texto para la generación del Libro Sueldo Digital
        Para una liquidación en particular
        Args:
            cuit: str, CUIT del empleador
            liquidacion_data: dict, datos de liquidación

        Retorna una tupla:
         - (Error bool, Error str, txt_data str)
         - False, error, None: si falla
         - True, None, txt_data: si todo salió bien
    """
    res_final = ''
    empleados_liquidados = liquidacion_data['empleados_liquidados']
    q_empleados = len(empleados_liquidados)
    tipo_liquidacion = liquidacion_data['tipo_liquidacion']
    fecha_pago = liquidacion_data['fecha_pago']
    fecha_pago_date = datetime.datetime.strptime(fecha_pago, '%Y-%m-%d').date()

    # Registro 1 -----------------------------------------------------------------------------------------
    registro1_txt = process_reg1(
        cuit=cuit,
        periodo=periodo,
        q_empleados=q_empleados,
        nro_liq=nro_liq,
        tipo_liq=tipo_liquidacion,
    )
    if not registro1_txt[0]:
        return False, registro1_txt[1], None

    res_final += registro1_txt[2]
    # Fin Registro 1 -------------------------------------------------------------------------------------

    # Registro 2 -----------------------------------------------------------------------------------------
    registro2_txt = process_reg2(
        empleados_liquidados=empleados_liquidados,
        fecha_pago=fecha_pago_date,
    )
    if not registro2_txt[0]:
        return False, registro2_txt[1], None
    res_final += registro2_txt[2]
    # Fin Registro 2 -------------------------------------------------------------------------------------

    # Registro 3 -----------------------------------------------------------------------------------------
    registro_3_por_empleado = []
    for empleado in empleados_liquidados:
        cuil = empleado['info_f931']['fijos']['cuil']
        conceptos_liquidados = empleado['info_f931']['variables']['conceptos_liquidados']
        this_registro3 = process_reg3(
            cuil=cuil,
            concepto_liq=conceptos_liquidados,
        )
        if not this_registro3[0]:
            return False, this_registro3[1], None
        registro_3_por_empleado.append(this_registro3[2])

    registro3_txt = '\r\n'.join(registro_3_por_empleado)
    res_final += registro3_txt[2]
    # Fin Registro 3 -------------------------------------------------------------------------------------

    # Registro 4 -----------------------------------------------------------------------------------------
    registro4_txt = process_reg4(
        empleados_liquidados=empleados_liquidados,
        fecha_pago=fecha_pago_date,
    )
    if not registro4_txt[0]:
        return False, registro4_txt[1], None
    res_final += registro4_txt[2]
    # Fin Registro 4 -------------------------------------------------------------------------------------

    # Registro 5 -----------------------------------------------------------------------------------------
    registro5_txt = process_reg5(
        empleados_liquidados=empleados_liquidados,
        fecha_pago=fecha_pago_date,
    )
    if not registro5_txt[0]:
        return False, registro5_txt[1], None
    res_final += registro5_txt[2]
    # Fin Registro 5 -------------------------------------------------------------------------------------

    return True, None, res_final


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

    # Inicio nro_liquidacion
    nro_liquidacion = 0
    for liquidacion in liquidaciones:
        if not isinstance(liquidacion, dict):
            return False, 'No se puede generar el txt, liquidaciones no es una lista de diccionarios'

        for indice in indices_esenciales_liquidaciones:
            if not liquidacion.get(indice):
                return False, f'No se puede generar el txt, dato esencial {indice} no encontrado en liquidaciones'

        nro_liquidacion += 1
        txt_liquidacion = genera_txt_lsd_liquidacion(
            cuit=cuit,
            periodo=periodo_date,
            liquidacion_data=liquidacion,
            nro_liq=nro_liquidacion,
        )

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
