import datetime
import os

from py_arg_reports.reporters.libro_sueldo_digital.generador_registros import (
    process_reg1,
    process_reg2,
    process_reg3,
    process_reg4,
    process_reg5,
)
from py_arg_reports.tools.tools import file_compress, delete_list_of_liles


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

    # Registro 3 y 4 -------------------------------------------------------------------------------------
    registro_3_por_empleado = []
    registro_4_por_empleado = []
    for empleado in empleados_liquidados:
        # Agrupo toda la informacion de info_931
        info_931 = {}
        info_931.update(empleado["info_f931"]["fijos"])
        info_931.update(empleado["info_f931"]["variables"])
        info_931.update(empleado["info_f931"]["importes"])

        cuil = info_931['cuil']
        conceptos_liquidados = empleado['conceptos_liquidados']
        this_registro3 = process_reg3(
            cuil=cuil,
            concepto_liq=conceptos_liquidados,
        )
        this_registro4 = process_reg4(
            cuil=cuil,
            info_931=info_931,
        )
        if not this_registro3[0]:
            return False, this_registro3[1], None
        registro_3_por_empleado.append(this_registro3[2])

        if not this_registro4[0]:
            return False, this_registro4[1], None
        registro_4_por_empleado.append(this_registro4[2])

    registro3_txt = '\r\n'.join(registro_3_por_empleado)
    registro4_txt = '\r\n'.join(registro_4_por_empleado)
    res_final += registro3_txt[2]
    res_final += registro4_txt[2]
    # Fin Registro 3 y 4 ---------------------------------------------------------------------------------

    # Registro 5 -----------------------------------------------------------------------------------------
    registro5_txt = process_reg5()
    if not registro5_txt[0]:
        return False, registro5_txt[1], None
    res_final += registro5_txt[2]
    # Fin Registro 5 -------------------------------------------------------------------------------------

    return True, None, res_final


def genera_archivo_final_lsd(txt_liquidaciones: list, output_path: str, filename: str) -> tuple:
    """ Genera el archivo de texto para la generación del Libro Sueldo Digital
        Args:
            txt_liquidaciones: list, lista de txt de liquidaciones
            output_path: str, ruta donde se guardará el archivo
            filename: str, nombre del archivo

        Retorna una tupla:
         - False, error, None: si falla
         - True, None, file_path: si todo salió bien
    """
    resp = None
    txt_liquidaciones_files = []

    # Voy escribiendo cada una de las liquidaciones
    for i, txt_liquidacion in enumerate(txt_liquidaciones):
        fpath = os.path.join(output_path, f'{filename}_{i}.txt')

        with open(fpath, 'w') as f:
            f.write(txt_liquidacion)

        txt_liquidaciones_files.append(fpath)

    if len(txt_liquidaciones) == 1:
        final_fpath = fpath
    else:
        zip_output_file_name = fpath = os.path.join(output_path, f'{filename}.zip')
        file_compress(txt_liquidaciones_files, zip_output_file_name)
        final_fpath = zip_output_file_name

        # Borro txts
        delete_list_of_liles(txt_liquidaciones_files)

    return True, resp, final_fpath


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
    txt_liquidaciones = []
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
        if not txt_liquidacion[0]:
            return False, txt_liquidacion[1]

        txt_liquidaciones.append(txt_liquidacion[2])

    # Genero el archivo final
    resultado_final = genera_archivo_final_lsd(
        txt_liquidaciones=txt_liquidaciones,
        output_path=output_path,
        filename=filename,
    )
    if not resultado_final[0]:
        return False, resultado_final[1]

    return True, resp
