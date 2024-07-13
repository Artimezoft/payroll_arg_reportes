import datetime


def process_reg2(empleados_liquidados: dict, fecha_pago: datetime.date) -> tuple:
    """ Generacion txt de Libro Sueldos Digital
        Registro 2 Datos referenciales de la Liquidación de SyJ del trabajador
        Args:
            empleados_liquidados: dict, datos de los empleados liquidados
            fecha_pago: datetime.date, fecha de la liquidacion
            Retorna:
            (Resultado, Error, Registro2)
            - True, None, str: si todo salió bien
            - False, str, None: si falla
    """
    resp = []
    keys_esenciales_empleado = ['empleado_legajo', 'info_f931']
    keys_esenciales_f931 = ['fijos', 'variables', 'importes']
    keys_esenciales_f931_fijos = ['cuil', 'forma_pago', 'cbu', 'area']
    # Formas de pago aceptadas
    # '1'=Efectivo; '2'=Cheque; '3'=Acreditación en cuenta

    for info_empleado in empleados_liquidados:
        # Validaciones
        for key in keys_esenciales_empleado:
            if key not in info_empleado:
                return False, f'Falta la clave {key} en el diccionario de empleados', None

        for key in keys_esenciales_f931:
            if key not in info_empleado['info_f931']:
                return False, f'Falta la clave {key} en el diccionario de F931', None

        for key in keys_esenciales_f931_fijos:
            if key not in info_empleado['info_f931']['fijos']:
                return False, f'Falta la clave {key} en el diccionario de F931 Fijos', None

        legajo = info_empleado['empleado_legajo']
        cuil = info_empleado['info_f931']['fijos']['cuil']
        cbu = info_empleado['info_f931']['fijos']['cbu']
        area = info_empleado['info_f931']['fijos']['area']
        forma_pago = info_empleado['info_f931']['fijos']['forma_pago']
        fecha_rubrica = " " * 8

        if forma_pago not in ['1', '2', '3']:
            return False, f'Forma de pago no válida para el empleado {legajo}', None

        if forma_pago == '3' and (not cbu or len(cbu) != 22):
            return False, f'Forma de pago Acreditación en cuenta CBU inválido {legajo}', None

        if forma_pago != '3':
            cbu = " " * 22

        # Normalizacion
        legajo_norm = str(legajo).zfill(10)
        area_norm = " " * 50 if not area else area.ljust(50)
        fecha_pago_str = fecha_pago('%Y%m%d')

        item = f'02{cuil}{legajo_norm}{area_norm}{cbu}030{fecha_pago_str}{fecha_rubrica}{forma_pago}'

        resp.append(item)

    # Listo los registros, los uno con \r\n
    resp_final = '\r\n'.join(resp)

    return True, None, resp_final
