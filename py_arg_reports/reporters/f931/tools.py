FORMATO_TXT_F931 = {
    'cuil': {'from': 1, 'long': 11, 'type': 'EN'},
    'nombre_completo': {'from': 12, 'long': 30, 'type': 'AL'},
    'conyuge': {'from': 42, 'long': 1, 'type': 'EN'},
    'hijos': {'from': 43, 'long': 2, 'type': 'EN'},
    'situacion': {'from': 45, 'long': 2, 'type': 'EN'},
    'condicion': {'from': 47, 'long': 2, 'type': 'EN'},
    'actividad': {'from': 49, 'long': 3, 'type': 'EN'},
    'zona': {'from': 52, 'long': 2, 'type': 'EN'},
    'porcentaje_aporte_adicional_ss': {'from': 54, 'long': 5, 'type': 'DE'},
    'modalidad_contrato': {'from': 59, 'long': 3, 'type': 'EN'},
    'obra_social': {'from': 62, 'long': 6, 'type': 'EN'},
    'adherentes': {'from': 68, 'long': 2, 'type': 'EN'},
    'remuneracion_total': {'from': 70, 'long': 12, 'type': 'DE'},
    'remuneracion_01': {'from': 82, 'long': 12, 'type': 'DE'},
    'asign_fam': {'from': 94, 'long': 9, 'type': 'DE'},
    'aporte_vol': {'from': 103, 'long': 9, 'type': 'DE'},
    'importe_adicional_os': {'from': 112, 'long': 9, 'type': 'DE'},
    'imp_exc_ap_ss': {'from': 121, 'long': 9, 'type': 'DE'},
    'imp_exc_ap_os': {'from': 130, 'long': 9, 'type': 'DE'},
    'localidad': {'from': 139, 'long': 50, 'type': 'AL'},
    'remuneracion_02': {'from': 189, 'long': 12, 'type': 'DE'},
    'remuneracion_03': {'from': 201, 'long': 12, 'type': 'DE'},
    'remuneracion_04': {'from': 213, 'long': 12, 'type': 'DE'},
    'codigo_siniestrado': {'from': 225, 'long': 2, 'type': 'EN'},
    'corresponde_reduccion': {'from': 227, 'long': 1, 'type': 'EN'},
    'capital_lrt': {'from': 228, 'long': 9, 'type': 'DE'},
    'tipo_empresa': {'from': 237, 'long': 1, 'type': 'EN'},
    'aporte_adicional_os': {'from': 238, 'long': 9, 'type': 'DE'},
    'regimen': {'from': 247, 'long': 1, 'type': 'EN'},
    'situacion_1': {'from': 248, 'long': 2, 'type': 'EN'},
    'dia_sr1': {'from': 250, 'long': 2, 'type': 'EN'},
    'situacion_2': {'from': 252, 'long': 2, 'type': 'EN'},
    'dia_sr2': {'from': 254, 'long': 2, 'type': 'EN'},
    'situacion_3': {'from': 256, 'long': 2, 'type': 'EN'},
    'dia_sr3': {'from': 258, 'long': 2, 'type': 'EN'},
    'sueldo': {'from': 260, 'long': 12, 'type': 'DE'},
    'sac': {'from': 272, 'long': 12, 'type': 'DE'},
    'hs_extras': {'from': 284, 'long': 12, 'type': 'DE'},
    'zona_desfavorable': {'from': 296, 'long': 12, 'type': 'DE'},
    'vacaciones': {'from': 308, 'long': 12, 'type': 'DE'},
    'k_dias': {'from': 320, 'long': 9, 'type': 'DE'},
    'remuneracion_05': {'from': 329, 'long': 12, 'type': 'DE'},
    'convencionado': {'from': 341, 'long': 1, 'type': 'EN'},
    'remuneracion_06': {'from': 342, 'long': 12, 'type': 'DE'},
    'tipo_operacion': {'from': 354, 'long': 1, 'type': 'EN'},
    'adicionales': {'from': 355, 'long': 12, 'type': 'DE'},
    'premios': {'from': 367, 'long': 12, 'type': 'DE'},
    'remuneracion_08': {'from': 379, 'long': 12, 'type': 'DE'},
    'remuneracion_07': {'from': 391, 'long': 12, 'type': 'DE'},
    'k_hs_extras': {'from': 403, 'long': 3, 'type': 'EN'},
    'no_remunerativo': {'from': 406, 'long': 12, 'type': 'DE'},
    'maternidad': {'from': 418, 'long': 12, 'type': 'DE'},
    'rectificacion': {'from': 430, 'long': 9, 'type': 'DE'},
    'remuneracion_09': {'from': 439, 'long': 12, 'type': 'DE'},
    'porc_contr_dif_ss': {'from': 451, 'long': 9, 'type': 'DE'},
    'k_horas': {'from': 460, 'long': 3, 'type': 'EN'},
    'seguro_vida_obligatorio': {'from': 463, 'long': 1, 'type': 'BO'},
    'detraccion': {'from': 464, 'long': 12, 'type': 'DE'},
    'incremento': {'from': 476, 'long': 12, 'type': 'DE'},
    'remuneracion_11': {'from': 488, 'long': 12, 'type': 'DE'},
}


def get_value_from_txt(txt_line: str, field_name: str) -> str:
    """ Retorna el valor de un campo en un txt de F931 de acuerdo a las
        posiciones del campo en el txt detalladas en FORMATO_TXT_F931
    """
    resp = ''

    if field_name in FORMATO_TXT_F931:
        resp = txt_line[FORMATO_TXT_F931[field_name]['from'] - 1:FORMATO_TXT_F931[field_name]['from'] - 1 +
                        FORMATO_TXT_F931[field_name]['long']].strip()

    return resp
