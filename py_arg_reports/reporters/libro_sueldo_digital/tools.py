FORMATO_TXT_LSD = {
    'registro1': {
        'tipo_registro': {'from': 1, 'long': 2, 'type': 'AL'},
        'cuit': {'from': 3, 'long': 11, 'type': 'EN'},
        'identificacion_envio': {'from': 14, 'long': 2, 'type': 'AL'},
        'periodo': {'from': 16, 'long': 6, 'type': 'EN'},
        'tipo_liquidacion': {'from': 22, 'long': 1, 'type': 'AL'},
        'numero_liquidacion': {'from': 23, 'long': 5, 'type': 'EN'},
        'dias_base': {'from': 28, 'long': 2, 'type': 'AL'},
        'cantidad_trabajadores': {'from': 30, 'long': 6, 'type': 'EN'},
    },
    'registro2': {
        'tipo_registro': {'from': 1, 'long': 2, 'type': 'AL'},
        'cuil': {'from': 3, 'long': 11, 'type': 'EN'},
        'legajo': {'from': 14, 'long': 10, 'type': 'EN'},
        'dependencia': {'from': 24, 'long': 50, 'type': 'AL'},
        'cbu': {'from': 74, 'long': 22, 'type': 'EN'},
        'dias_tope': {'from': 96, 'long': 3, 'type': 'EN'},
        'fecha_pago': {'from': 99, 'long': 8, 'type': 'FE'},
        'fecha_rubrica': {'from': 107, 'long': 8, 'type': 'FE'},
        'forma_pago': {'from': 115, 'long': 1, 'type': 'AL'},
    },
    'registro3': {
        'tipo_registro': {'from': 1, 'long': 2, 'type': 'AL'},
        'cuil': {'from': 3, 'long': 13, 'type': 'EN'},
        'codigo_concepto': {'from': 16, 'long': 10, 'type': 'EN'},
        'cantidad': {'from': 26, 'long': 5, 'type': 'EN'},
        'unidades': {'from': 31, 'long': 1, 'type': 'EN'},
        'importe': {'from': 32, 'long': 15, 'type': 'DE'},
        'indicador': {'from': 47, 'long': 1, 'type': 'AL'},
        'periodo_ajuste': {'from': 48, 'long': 6, 'type': 'EN'},
    },
    'registro4': {
        'tipo_registro': {'from': 1, 'long': 2, 'type': 'AL'},
        'cuil': {'from': 3, 'long': 11, 'type': 'EN'},
        'conyuge': {'from': 14, 'long': 1, 'type': 'EN'},
        'hijos': {'from': 15, 'long': 2, 'type': 'EN'},
        'cct': {'from': 17, 'long': 1, 'type': 'AL'},
        'svo': {'from': 18, 'long': 1, 'type': 'AL'},
        'reduccion': {'from': 19, 'long': 1, 'type': 'AL'},
        'tipo_empleador': {'from': 20, 'long': 1, 'type': 'AL'},
        'tipo_operacion': {'from': 21, 'long': 1, 'type': 'AL'},
        'situacion_revista': {'from': 22, 'long': 2, 'type': 'AL'},
        'condicion': {'from': 24, 'long': 2, 'type': 'AL'},
        'actividad': {'from': 26, 'long': 3, 'type': 'AL'},
        'modalidad_contratacion': {'from': 29, 'long': 3, 'type': 'AL'},
        'siniestrado': {'from': 32, 'long': 2, 'type': 'AL'},
        'localidad': {'from': 34, 'long': 2, 'type': 'AL'},
        'situacion_revista_1': {'from': 36, 'long': 2, 'type': 'AL'},
        'dia_sr1': {'from': 38, 'long': 2, 'type': 'EN'},
        'situacion_revista_2': {'from': 40, 'long': 2, 'type': 'AL'},
        'dia_sr2': {'from': 42, 'long': 2, 'type': 'EN'},
        'situacion_revista_3': {'from': 44, 'long': 2, 'type': 'AL'},
        'dia_sr3': {'from': 46, 'long': 2, 'type': 'EN'},
        'dias_trabajados': {'from': 48, 'long': 2, 'type': 'EN'},
        'horas_trabajadas': {'from': 50, 'long': 3, 'type': 'EN'},
        'porcentaje_aporte_adicional_ss': {'from': 53, 'long': 5, 'type': 'DE'},
        'porcentaje_contribucion_diferencial': {'from': 58, 'long': 5, 'type': 'DE'},
        'obra_social': {'from': 63, 'long': 6, 'type': 'AL'},
        'adherentes': {'from': 69, 'long': 2, 'type': 'EN'},
        'aporte_adicional_os': {'from': 71, 'long': 15, 'type': 'DE'},
        'contribucion_adicional_os': {'from': 86, 'long': 15, 'type': 'DE'},
        'base_calculo_diferencial_aporte_os': {'from': 101, 'long': 15, 'type': 'DE'},
        'base_calculo_diferencial_contribucion_os': {'from': 116, 'long': 15, 'type': 'DE'},
        'base_calculo_diferencial_lrt': {'from': 131, 'long': 15, 'type': 'DE'},
        'remuneracion_maternidad_anses': {'from': 146, 'long': 15, 'type': 'DE'},
        'remuneracion_bruta': {'from': 161, 'long': 15, 'type': 'DE'},
        'base_imponible_1': {'from': 176, 'long': 15, 'type': 'DE'},
        'base_imponible_2': {'from': 191, 'long': 15, 'type': 'DE'},
        'base_imponible_3': {'from': 206, 'long': 15, 'type': 'DE'},
        'base_imponible_4': {'from': 221, 'long': 15, 'type': 'DE'},
        'base_imponible_5': {'from': 236, 'long': 15, 'type': 'DE'},
        'base_imponible_6': {'from': 251, 'long': 15, 'type': 'DE'},
        'base_imponible_7': {'from': 266, 'long': 15, 'type': 'DE'},
        'base_imponible_8': {'from': 281, 'long': 15, 'type': 'DE'},
        'base_imponible_9': {'from': 296, 'long': 15, 'type': 'DE'},
        'base_calculo_diferencial_aporte_ss': {'from': 311, 'long': 15, 'type': 'DE'},
        'base_calculo_diferencial_contribucion_ss': {'from': 326, 'long': 15, 'type': 'DE'},
        'base_imponible_10': {'from': 341, 'long': 15, 'type': 'DE'},
        'importe_detraer': {'from': 356, 'long': 15, 'type': 'DE'},
    },
    'registro5': {
        'tipo_registro': {'from': 1, 'long': 2, 'type': 'AL'},
        'cuil': {'from': 3, 'long': 11, 'type': 'EN'},
        'categoria_profesional': {'from': 14, 'long': 6, 'type': 'EN'},
        'puesto_desempenado': {'from': 20, 'long': 4, 'type': 'AL'},
        'fecha_ingreso': {'from': 24, 'long': 8, 'type': 'FE'},
        'fecha_egreso': {'from': 32, 'long': 8, 'type': 'FE'},
        'remuneracion': {'from': 40, 'long': 15, 'type': 'DE'},
        'cuit_empleador': {'from': 55, 'long': 11, 'type': 'EN'},
    },
}


def get_value_from_txt(txt_line: str, nro_reg: int, field_name: str) -> str:
    """ Retorna el valor de un campo en un txt de Libro Sueldo Digital de acuerdo a las
        especificaciones de AFIP.
    """
    resp = ''
    where_to_look = FORMATO_TXT_LSD['registro' + str(nro_reg)]

    if field_name in where_to_look:
        resp = txt_line[where_to_look[field_name]['from'] - 1:where_to_look[field_name]['from'] - 1 +
                        where_to_look[field_name]['long']].strip()

    return resp
