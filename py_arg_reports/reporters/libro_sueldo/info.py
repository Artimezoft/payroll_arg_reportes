from py_arg_reports.tools.recibos_utils import (
    float_to_format_currency,
    formatted_date_str,
)


def get_recibo_info(json_data: dict) -> dict:
    """ Obtiene la información del recibo de sueldo en formato JSON
        Con datos de la empresa, empleado, liquidación, etc.
        con el formato en el ejemplo reporters/samples/samples-recibo-info.json
        # TODO esto es igual a reporters.recibo_sueldo.get_recibo_info, ver si se puede unificar
    """
    # Si el json está vacío, no se puede descargar
    if not json_data:
        return {
            "error": "No se puede descargar el recibo, no hay datos"
        }

    # Si faltan algunas de las keys en results, no se puede descargar
    keys_to_check = ['empresa', 'liquidacion', 'empleado', 'conceptos_liquidados', 'totales_liquidacion']
    for key in keys_to_check:
        if key not in json_data[0]:
            return {
                "error": f"No se puede descargar el recibo, no se observa {key} en los datos"
            }

    resp = {
        "empresa": {},
        "liquidacion": {},
        "empleados": {},
        "conceptos_liquidados": [],
        'totales_liquidacion': {},
        "error": "",
    }

    serialized_emp_liqs = json_data

    # Empresa info ---------------------------------------------------------------------------
    empresa_info = serialized_emp_liqs[0]['empresa']
    resp["empresa"] = empresa_info

    # Liquidación info -----------------------------------------------------------------------
    liquidacion_info = serialized_emp_liqs[0]['liquidacion']
    resp["liquidacion"] = liquidacion_info

    # Empleados info -------------------------------------------------------------------------
    empleado_list = [item['empleado'] for item in serialized_emp_liqs]
    resp["empleados"] = empleado_list

    # Conceptos info -------------------------------------------------------------------------
    conceptos_dict = {}
    totales_liquidacion_dict = {}
    for emp_liq in serialized_emp_liqs:
        legajo = emp_liq['empleado']['legajo']
        conceptos_liquidados = emp_liq['conceptos_liquidados']
        this_conceptos = []
        for concepto in conceptos_liquidados:
            code = concepto['concepto']['code']
            name = concepto['concepto']['name']
            tipo_concepto = concepto['concepto']['tipo_concepto']
            cantidad = concepto['cantidad']
            importe = concepto['importe']
            this_conceptos.append({
                'code': code,
                'name': name,
                'tipo_concepto': tipo_concepto,
                'cantidad': cantidad,
                'importe': importe,
            })

        conceptos_dict[str(legajo)] = this_conceptos
        totales_liquidacion_dict[str(legajo)] = emp_liq['totales_liquidacion']

    resp["conceptos_liquidados"] = conceptos_dict
    resp["totales_liquidacion"] = totales_liquidacion_dict

    return resp


def get_info_final_for_libro_sueldo(api_dict: dict) -> dict:
    """
    # TODO esto es igual a reporters.recibo_sueldo.get_info_final_for_recibo, ver si se puede unificar
    """
    periodo = api_dict["liquidacion"]["periodo"]["periodo"]
    tipo_liquidacion = api_dict["liquidacion"]["tipo_liquidacion"]
    company_name = api_dict["empresa"]["name"]
    cuit = api_dict["empresa"]["cuit"]
    domicilio_obj = api_dict["empresa"]["domicilio"]
    domicilio = domicilio_obj["calle"] + ' ' + domicilio_obj["numero"]
    domicilio_elements_to_add = ['piso', 'oficina', 'barrio']
    for element in domicilio_elements_to_add:
        if domicilio_obj[element]:
            domicilio += ', ' + domicilio_obj[element]

    localidad = domicilio_obj["localidad"]["name"]
    provincia = domicilio_obj["localidad"]["provincia"]["name"]
    domicilio += f', {localidad}, {provincia}'

    periodo = api_dict["liquidacion"]["periodo"]["periodo"]
    tipo_liquidacion = api_dict["liquidacion"]["tipo_liquidacion"]
    fecha_pago = formatted_date_str(api_dict["liquidacion"]["fecha_pago"])
    ultimo_pago_ss = api_dict["empresa"]["ultimo_pago_seguridad_social"]

    # Datos que varían por página, todos van a ser diccionarios con la key con el legajo, salvo el mismo legajo
    legajos = []
    nombres_completos = {}
    cuiles = {}
    categorias = {}
    fechas_ingreso = {}
    fechas_ingreso_2 = {}
    contratos = {}
    obras_sociales = {}
    areas = {}
    posiciones = {}
    basicos = {}
    lugares_trabajo = {}
    relaciones_bancarias = {}
    conceptos_liquidados = {}
    totales_liquidacion = {}

    for empleado in api_dict['empleados']:
        legajo = str(empleado["legajo"])
        legajos.append(legajo)

        nombre = empleado["first_name"]
        apellido = empleado["last_name"]
        nombre_completo = f'{apellido}, {nombre}'
        nombres_completos[legajo] = nombre_completo.upper()

        cuil = empleado["cuil"]
        cuil = f'{cuil[:2]}-{cuil[2:10]}-{cuil[10:]}'
        cuiles[legajo] = cuil

        categorias[legajo] = empleado["categoria"]
        fecha_ingreso = api_dict["empleados"][0]["fecha_ingreso"]
        fecha_ingreso = formatted_date_str(fecha_ingreso)
        fechas_ingreso[legajo] = fecha_ingreso
        fecha_ingreso_2 = api_dict["empleados"][0]["fecha_ingreso_2"]
        if fecha_ingreso_2:
            fechas_ingreso_2[legajo] = formatted_date_str(fecha_ingreso_2)
        contratos[legajo] = empleado["contrato"]
        obras_sociales[legajo] = empleado["obra_social"]
        areas[legajo] = empleado["area"]
        posiciones[legajo] = empleado["posicion"]
        basicos[legajo] = float_to_format_currency(empleado["basico"])
        lugares_trabajo[legajo] = empleado["lugar_trabajo"]
        relaciones_bancarias[legajo] = empleado["relacion_bancaria"]

        conceptos_liquidados = api_dict["conceptos_liquidados"]
        totales_liquidacion = api_dict["totales_liquidacion"]

    resp = {
        # Período y Compañía
        "periodo": periodo,
        "company_name": company_name,
        "cuit": cuit,
        "domicilio": domicilio,
        "tipo_liquidacion": tipo_liquidacion,

        # Empleados
        "nombres_completos": nombres_completos,
        'cuiles': cuiles,
        'legajos': legajos,
        "categorias": categorias,
        "fechas_ingreso": fechas_ingreso,
        "fechas_ingreso_2": fechas_ingreso_2,
        "contratos": contratos,
        "obras_sociales": obras_sociales,
        "areas": areas,
        "posiciones": posiciones,
        "basicos": basicos,
        "lugares_trabajo": lugares_trabajo,

        # Conceptos
        "conceptos_liquidados": conceptos_liquidados,
        'totales_liquidacion': totales_liquidacion,

        # Pie de página
        "fecha_pago": fecha_pago,
        "ultimo_pago_ss": ultimo_pago_ss,
        "relaciones_bancarias": relaciones_bancarias,
    }
    return resp

