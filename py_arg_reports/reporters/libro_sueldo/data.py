"""
Process data from origin to what we need
"""
from py_arg_reports.tools.recibos_utils import (
    float_to_format_currency,
    formatted_date_str,
)


def translate_data(origin_data):

    resp = {}
    # Tomo los datos de la primera empresa (espero que sean todas iguales)
    if len(origin_data) == 0:
        raise ValueError("No hay datos para procesar (se espera al menos un empleado)")
    empresa = origin_data[0]['empresa']

    liquidacion = origin_data[0]['liquidacion']
    empleados = [emp for emp in origin_data]
    legajos = [emp['empleado']['legajo'] for emp in empleados]
    # Veo lo que realmente necesita el PDF
    resp = {
        'company_name': get_company_name(empresa),
        'domicilio': get_domicilio_empresa(empresa),
        'cuit': get_cuit(empresa),
        'actividad_principal': get_actividad_principal(empresa),  # TODO
        'actividades_secundarias': get_actividad_secundarias(empresa),
        'tipo_liquidacion': get_tipo_liquidacion(liquidacion),
        'periodo': get_periodo_liquidacon(liquidacion),
        'legajos': legajos,
        'empleados': []
    }
    for emp in empleados:
        empleado = emp['empleado']
        conceptos_liquidados = emp['conceptos_liquidados']
        liquidacion = emp['liquidacion']
        totales_liquidacion = emp['totales_liquidacion']
        resp['empleados'].append(
            {
                'nombre': get_nombre_empleado(empleado),
                'cuil': get_cuil_empleado(empleado),
                'legajo': empleado['legajo'],
                'estado_civil': get_estado_civil(empleado),
                'categoria': empleado.get('categoria', ''),
                'fecha_ingreso': get_nice_fecha(empleado.get('fecha_ingreso')),
                'fecha_ingreso_2': get_nice_fecha(empleado.get('fecha_ingreso_2')),
                'contrato': empleado.get('contrato', ''),
                'obra_social': empleado.get('obra_social', ''),
                'area': empleado.get('area', ''),
                'posicion': empleado.get('posicion', ''),
                'basico': get_empleado_basico(empleado),
                'lugar_trabajo': empleado.get('lugar_trabajo', ''),
                'conceptos_liquidados': get_conceptos_liquidados(conceptos_liquidados),
                'totales_liquidacion': totales_liquidacion,
                'relacion_bancaria': get_relacion_bancaria(empleado),
            },
        )
    return resp


def get_company_name(empresa):
    return empresa['name']


def get_domicilio_empresa(empresa):
    domicilio_obj = empresa['domicilio']
    domicilio = domicilio_obj.get('calle', '') + ' ' + domicilio_obj.get('numero', '')
    domicilio_elements_to_add = ['piso', 'oficina', 'barrio']
    for element in domicilio_elements_to_add:
        if domicilio_obj.get(element):
            domicilio += ', ' + domicilio_obj.get(element)

    localidad = domicilio_obj["localidad"]["name"]
    provincia = domicilio_obj["localidad"]["provincia"]["name"]
    domicilio += f', {localidad}, {provincia}'
    return domicilio


def get_cuit(empresa):
    return empresa['cuit']


def get_actividad_principal(empresa):
    # tomar el dato de actividad principal de la empresa
    return empresa['actividad_principal']


def get_actividad_secundarias(empresa):
    # tomar el dato de actividad secundaria de la empresa
    return empresa['actividades_secundarias']


def get_liquidacion(liquidacion):
    """ Obtener UNA liquidacion de un empleado """
    fecha_pago = formatted_date_str(liquidacion.get('fecha_pago'))
    ret = {
        'nro_liquidacion': liquidacion.get('nro_liquidacion'),
        'tipo_liquidacion': liquidacion.get('tipo_liquidacion'),
        'periodo': liquidacion.get('periodo', {}).get('periodo'),
        'fecha_pago': fecha_pago,
    }
    return ret


def get_tipo_liquidacion(liquidacion):
    """ Datos de liquidacion gewnerica (esperamos todas iguales) """
    return liquidacion['tipo_liquidacion']


def get_periodo_liquidacon(liquidacion):
    """ Datos de liquidacion gewnerica (esperamos todas iguales) """
    return liquidacion['periodo']['periodo']


def get_nombre_empleado(empleado):
    nombre = empleado['first_name']
    apellido = empleado['last_name']
    return f'{apellido}, {nombre}'


def get_cuil_empleado(empleado):
    cuil = empleado['cuil']
    return f'{cuil[:2]}-{cuil[2:10]}-{cuil[10:]}'


def get_conceptos_liquidados(conceptos):
    new_conceptos = []
    for concepto in conceptos:
        new_conceptos.append(
            {
                'code': concepto['concepto']['code'],
                'name': concepto['concepto']['name'],
                'tipo_concepto': concepto['concepto']['tipo_concepto'],
                'cantidad': concepto['cantidad'],
                'importe': concepto['importe'],
                'orden': concepto.get('orden', 99),
            }
        )

    return new_conceptos


def get_relacion_bancaria(empleado):
    return empleado.get('relacion_bancaria', {})


def get_empleado_basico(empleado):
    return float_to_format_currency(empleado.get('basico', 0))


def get_nice_fecha(fecha_str):
    if fecha_str:
        return formatted_date_str(fecha_str)
    return ''


def get_estado_civil(empleado):
    estado_civil = empleado.get('marital_status', 'Dato no disponible')
    return estado_civil
