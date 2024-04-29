from numero_a_letras import numero_a_letras
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from py_arg_reports.config import config_constants
from py_arg_reports.tools.recibos_utils import (
    draw_text_with_end_coordinate,
    draw_text_with_max_width,
    float_to_format_currency,
    formatted_date_str,
    nombre_mes,
)


FONT_FAMILY = config_constants['FONT_FAMILY']
FONT_FAMILY_BOLD = config_constants['FONT_FAMILY_BOLD']
FONT_SIZE_MAIN = config_constants['FONT_SIZE_MAIN']
FONT_SIZE_BODY = config_constants['FONT_SIZE_BODY']


def get_coordinates_for_libro_sueldo(my_recibo_info: dict) -> dict:
    first_line_y = my_recibo_info['company_info_y'] + my_recibo_info['company_info_height'] - 0.35 * cm
    base_x = 0.2 * cm
    base_duplicate_x = my_recibo_info['duplicate_x'] + 0.2 * cm
    base_x_ends = base_x + my_recibo_info['employee_info_width'] - 0.4 * cm
    base_duplicate_x_ends = base_duplicate_x + my_recibo_info['employee_info_width'] - 0.4 * cm
    base_line_between = 0.5 * cm
    base_line_between_2 = 0.43 * cm
    starting_y_employee_info = my_recibo_info['employee_info_y'] + my_recibo_info['employee_info_height'] - 0.45 * cm

    starting_y_conceptos = my_recibo_info['conceptos_titles_y'] - 0.45 * cm

    resp = {
        'company_x': base_x,
        'company_y': first_line_y,
        'company_domicilio_x': base_x,
        'company_domicilio_y': first_line_y - base_line_between,
        'company_cuit_x': base_x,
        'company_cuit_y': first_line_y - base_line_between * 2,

        'dupl_company_x': base_duplicate_x,
        'dupl_company_domicilio_x': base_duplicate_x,
        'dupl_company_cuit_x': base_duplicate_x,

        'liquidacion_info_x': my_recibo_info['liquidacion_info_x'] + my_recibo_info['liquidacion_info_width'] / 4,
        'liquidacion_info_y': first_line_y - 0.1 * cm,
        'periodo_x': my_recibo_info['liquidacion_info_x'] + my_recibo_info['liquidacion_info_width'] / 4,
        'periodo_y': first_line_y - 0.8 * cm,

        'dupl_liq_info_x': my_recibo_info['liquidacion_info_x_duplicate'] + my_recibo_info['liquidacion_info_width'] / 4,
        'dupl_periodo_x': my_recibo_info['liquidacion_info_x_duplicate'] + my_recibo_info['liquidacion_info_width'] / 4,

        'nombre_x': base_x,
        'nombre_y': starting_y_employee_info,
        'categoria_x': base_x,
        'categoria_y': starting_y_employee_info - base_line_between_2,
        'posicion_x': base_x,
        'posicion_y': starting_y_employee_info - base_line_between_2 * 2,
        'area_x': base_x,
        'area_y': starting_y_employee_info - base_line_between_2 * 3,
        'contrato_x': base_x,
        'contrato_y': starting_y_employee_info - base_line_between_2 * 4,
        'obra_social_x': base_x,
        'obra_social_y': starting_y_employee_info - base_line_between_2 * 5,
        'legajo_e_ingreso_x_ends': base_x_ends,
        'legajo_e_ingreso_y': starting_y_employee_info,
        'cuil_x_ends': base_x_ends,
        'cuil_y': starting_y_employee_info - base_line_between_2,
        'basico_x_ends': base_x_ends,
        'basico_y': starting_y_employee_info - base_line_between_2 * 2,
        'fecha_ingreso_2_x_ends': base_x_ends,
        'fecha_ingreso_2_y': starting_y_employee_info - base_line_between_2 * 3,

        'dupl_nombre_x': base_duplicate_x,
        'dupl_categoria_x': base_duplicate_x,
        'dupl_posicion_x': base_duplicate_x,
        'dupl_area_x': base_duplicate_x,
        'dupl_contrato_x': base_duplicate_x,
        'dupl_obra_social_x': base_duplicate_x,
        'dupl_legajo_e_ingreso_x_ends': base_duplicate_x_ends,
        'dupl_cuil_x_ends': base_duplicate_x_ends,
        'dupl_basico_x_ends': base_duplicate_x_ends,
        'dupl_fecha_ingreso_2_x_ends': base_duplicate_x_ends,

        'starting_y_conceptos': starting_y_conceptos,
        'conceptos_x': base_x,
        'dupl_conceptos_x': base_duplicate_x,
        'concepto_titles_x_cant': my_recibo_info['concepto_titles_x_cant'],
        'concepto_titles_x_rem': my_recibo_info['concepto_titles_x_rem'],
        'concepto_titles_x_nr': my_recibo_info['concepto_titles_x_nr'],
        'concepto_titles_x_ap': my_recibo_info['concepto_titles_x_ap'],
        'dupl_concepto_titles_x_cant': my_recibo_info['dupl_concepto_titles_x_cant'],
        'dupl_concepto_titles_x_rem': my_recibo_info['dupl_concepto_titles_x_rem'],
        'dupl_concepto_titles_x_nr': my_recibo_info['dupl_concepto_titles_x_nr'],
        'dupl_concepto_titles_x_ap': my_recibo_info['dupl_concepto_titles_x_ap'],

        'concepto_titles_x_cant_ends': my_recibo_info['concepto_titles_x_rem'],
        'concepto_titles_x_rem_ends': my_recibo_info['concepto_titles_x_nr'],
        'concepto_titles_x_nr_ends': my_recibo_info['concepto_titles_x_ap'],
        'concepto_titles_x_ap_ends': base_x_ends,
        'dupl_concepto_titles_x_cant_ends': my_recibo_info['dupl_concepto_titles_x_rem'],
        'dupl_concepto_titles_x_rem_ends': my_recibo_info['dupl_concepto_titles_x_nr'],
        'dupl_concepto_titles_x_nr_ends': my_recibo_info['dupl_concepto_titles_x_ap'],
        'dupl_concepto_titles_x_ap_ends': base_duplicate_x_ends,
        'starting_y_totales': my_recibo_info['starting_y_totales'],
        'starting_y_totales_neto': my_recibo_info['starting_y_totales_neto'],
        'totales_x_rem': my_recibo_info['concepto_titles_x_rem'],
        'totales_x_nr': my_recibo_info['concepto_titles_x_nr'],
        'totales_x_ap': my_recibo_info['concepto_titles_x_ap'],
        'neto_letras_y': my_recibo_info['starting_y_totales_neto'] - base_line_between_2 + 0.05 * cm,

        'pie_de_pagina_x': base_x,
        'dupl_pie_de_pagina_x': base_duplicate_x,
        'pie_de_pagina_y': my_recibo_info['pie_pagina_y'],
        'pie_de_pagina_width': my_recibo_info['pie_pagina_width'],
        'pie_de_pagina_height': my_recibo_info['pie_pagina_height'],
    }

    return resp


def draw_empleado(c: canvas.Canvas, coordinates: dict, info_recibo: dict, legajo: str) -> str:
    # Variables Base ----------------------------------------------------------------------------
    base_line_between = 0.5 * cm

    # Company name -------------------------------------------------------------------------------
    # Original
    c.setFont(FONT_FAMILY_BOLD, FONT_SIZE_MAIN)
    c.drawString(coordinates['company_x'], coordinates['company_y'], info_recibo['company_name'])
    c.setFont(FONT_FAMILY, FONT_SIZE_MAIN)
    c.drawString(coordinates['company_domicilio_x'], coordinates['company_domicilio_y'], info_recibo['domicilio'])
    c.drawString(coordinates['company_cuit_x'], coordinates['company_cuit_y'], f'CUIT: {info_recibo["cuit"]}')

    # Duplicate
    c.setFont(FONT_FAMILY_BOLD, FONT_SIZE_MAIN)
    c.drawString(coordinates['dupl_company_x'], coordinates['company_y'], info_recibo['company_name'])
    c.setFont(FONT_FAMILY, FONT_SIZE_MAIN)
    c.drawString(coordinates['dupl_company_domicilio_x'], coordinates['company_domicilio_y'],
                 info_recibo['domicilio'])
    c.drawString(coordinates['dupl_company_cuit_x'], coordinates['company_cuit_y'],
                 f'CUIT: {info_recibo["cuit"]}')

    # End of Company name -------------------------------------------------------------------------

    # Liquidación Info ----------------------------------------------------------------------------
    # Original
    c.drawString(coordinates['liquidacion_info_x'], coordinates['liquidacion_info_y'],
                 info_recibo['tipo_liquidacion'])
    c.drawString(coordinates['periodo_x'], coordinates['periodo_y'], info_recibo['periodo'])

    # Duplicate
    c.drawString(coordinates['dupl_liq_info_x'], coordinates['liquidacion_info_y'],
                 info_recibo['tipo_liquidacion'])
    c.drawString(coordinates['dupl_periodo_x'], coordinates['periodo_y'], info_recibo['periodo'])

    # End of Liquidación Info ---------------------------------------------------------------------

    # From now on font size 8
    c.setFont(FONT_FAMILY, FONT_SIZE_BODY)

    # Employee Info -------------------------------------------------------------------------------
    # Información del empleado
    nombre_completo = info_recibo['nombres_completos'][legajo]
    categoria = info_recibo['categorias'][legajo]
    posicion = info_recibo['posiciones'][legajo]
    area = info_recibo['areas'][legajo]
    contrato = info_recibo['contratos'][legajo]
    obra_social = info_recibo['obras_sociales'][legajo]
    cuil = info_recibo['cuiles'][legajo]
    fecha_ingreso = info_recibo['fechas_ingreso'][legajo]
    fecha_ingreso_2 = info_recibo['fechas_ingreso_2'].get(legajo)
    basico = info_recibo['basicos'][legajo]
    lugar_trabajo = info_recibo['lugares_trabajo'][legajo]

    # Original
    c.drawString(coordinates['nombre_x'], coordinates['nombre_y'], f"Nombre: {nombre_completo}")
    c.drawString(coordinates['categoria_x'], coordinates['categoria_y'], f"Categoria: {categoria}")
    c.drawString(coordinates['posicion_x'], coordinates['posicion_y'], f"Posición: {posicion}")
    c.drawString(coordinates['area_x'], coordinates['area_y'], f"Area: {area}")
    c.drawString(coordinates['contrato_x'], coordinates['contrato_y'], f"Contrato: {contrato}")
    c.drawString(coordinates['obra_social_x'], coordinates['obra_social_y'], f"O.Social: {obra_social}")
    draw_text_with_end_coordinate(
        canvas=c,
        x_end=coordinates['legajo_e_ingreso_x_ends'],
        y=coordinates['legajo_e_ingreso_y'],
        text=f"Legajo: {legajo} - Ingreso: {fecha_ingreso}",
    )
    draw_text_with_end_coordinate(
        canvas=c,
        x_end=coordinates['cuil_x_ends'],
        y=coordinates['cuil_y'],
        text=f"CUIL: {cuil}",
    )
    draw_text_with_end_coordinate(
        canvas=c,
        x_end=coordinates['basico_x_ends'],
        y=coordinates['basico_y'],
        text=f"Remuneración Asignada: {basico}",
    )
    if fecha_ingreso_2:
        draw_text_with_end_coordinate(
            canvas=c,
            x_end=coordinates['fecha_ingreso_2_x_ends'],
            y=coordinates['fecha_ingreso_2_y'],
            text=f"Fecha Ing. Reconocida: {fecha_ingreso_2}",
        )

    # Duplicate
    c.drawString(coordinates['dupl_nombre_x'], coordinates['nombre_y'], f"Nombre: {nombre_completo}")
    c.drawString(coordinates['dupl_categoria_x'], coordinates['categoria_y'], f"Categoria: {categoria}")
    c.drawString(coordinates['dupl_posicion_x'], coordinates['posicion_y'], f"Posición: {posicion}")
    c.drawString(coordinates['dupl_area_x'], coordinates['area_y'], f"Area: {area}")
    c.drawString(coordinates['dupl_contrato_x'], coordinates['contrato_y'], f"Contrato: {contrato}")
    c.drawString(coordinates['dupl_obra_social_x'], coordinates['obra_social_y'], f"O.Social: {obra_social}")
    draw_text_with_end_coordinate(
        canvas=c,
        x_end=coordinates['dupl_legajo_e_ingreso_x_ends'],
        y=coordinates['legajo_e_ingreso_y'],
        text=f"Legajo: {legajo} - Ingreso: {fecha_ingreso}",
    )
    draw_text_with_end_coordinate(
        canvas=c,
        x_end=coordinates['dupl_cuil_x_ends'],
        y=coordinates['cuil_y'],
        text=f"CUIL: {cuil}",
    )
    draw_text_with_end_coordinate(
        canvas=c,
        x_end=coordinates['dupl_basico_x_ends'],
        y=coordinates['basico_y'],
        text=f"Remuneración Asignada: {basico}",
    )
    if fecha_ingreso_2:
        draw_text_with_end_coordinate(
            canvas=c,
            x_end=coordinates['dupl_fecha_ingreso_2_x_ends'],
            y=coordinates['fecha_ingreso_2_y'],
            text=f"Fecha Ing. Reconocida: {fecha_ingreso_2}",
        )

    # End of Employee Info ------------------------------------------------------------------------

    # Conceptos ----------------------------------------------------------------------------------
    conceptos_liquidados = info_recibo['conceptos_liquidados'][legajo]
    this_y = coordinates['starting_y_conceptos']
    for concepto in conceptos_liquidados:
        # code = concepto['code']
        name = concepto['name']
        tipo_concepto = concepto['tipo_concepto']
        cantidad = concepto['cantidad']
        importe = concepto['importe']
        # Si tipo de no es ni 1, ni 2, ni 3, no se muestra
        # Si bien no debería pasar por el filtro del QS, por las dudas
        if tipo_concepto not in [1, 2, 3]:
            continue

        # TODO: Ver si conviene agregar code
        c.drawString(coordinates['conceptos_x'], this_y, name)
        c.drawString(coordinates['concepto_titles_x_cant'], this_y, str(cantidad))

        c.drawString(coordinates['dupl_conceptos_x'], this_y, name)
        c.drawString(coordinates['dupl_concepto_titles_x_cant'], this_y, str(cantidad))

        if tipo_concepto == 1:
            x_to_use = coordinates['concepto_titles_x_rem_ends']
            x_to_use_dupl = coordinates['dupl_concepto_titles_x_rem_ends']
        elif tipo_concepto == 2:
            x_to_use = coordinates['concepto_titles_x_nr_ends']
            x_to_use_dupl = coordinates['dupl_concepto_titles_x_nr_ends']
        elif tipo_concepto == 3:
            x_to_use = coordinates['concepto_titles_x_ap_ends']
            x_to_use_dupl = coordinates['dupl_concepto_titles_x_ap_ends']

        draw_text_with_end_coordinate(
            canvas=c,
            x_end=x_to_use,
            y=this_y,
            text=float_to_format_currency(importe, include_currency=False),
        )
        draw_text_with_end_coordinate(
            canvas=c,
            x_end=x_to_use_dupl,
            y=this_y,
            text=float_to_format_currency(importe, include_currency=False),
        )
        this_y -= 0.4 * cm
    # End of Conceptos ----------------------------------------------------------------------------

    # Totales ----------------------------------------------------------------------------
    totales_remunerativo = info_recibo['totales_liquidacion'][legajo]['total_remunerativo']
    totales_no_remunerativo = info_recibo['totales_liquidacion'][legajo]['total_no_remunerativo']
    totales_retenciones = info_recibo['totales_liquidacion'][legajo]['total_retenciones']
    neto_liquidacion = info_recibo['totales_liquidacion'][legajo]['neto_liquidacion']
    neto_en_letras = numero_a_letras(neto_liquidacion)

    # Original
    c.drawString(coordinates['totales_x_rem'], coordinates['starting_y_totales'],
                 float_to_format_currency(totales_remunerativo, include_currency=False))
    c.drawString(coordinates['totales_x_nr'], coordinates['starting_y_totales'],
                 float_to_format_currency(totales_no_remunerativo, include_currency=False))
    c.drawString(coordinates['totales_x_ap'], coordinates['starting_y_totales'],
                 float_to_format_currency(totales_retenciones, include_currency=False))
    c.setFont(FONT_FAMILY_BOLD, FONT_SIZE_MAIN)
    c.drawString(coordinates['totales_x_ap'] - 0.5 * cm, coordinates['starting_y_totales_neto'],
                 float_to_format_currency(neto_liquidacion, include_currency=False))
    c.setFont(FONT_FAMILY, FONT_SIZE_BODY)

    # Duplicate
    c.drawString(coordinates['dupl_concepto_titles_x_rem'], coordinates['starting_y_totales'],
                 float_to_format_currency(totales_remunerativo, include_currency=False))
    c.drawString(coordinates['dupl_concepto_titles_x_nr'], coordinates['starting_y_totales'],
                 float_to_format_currency(totales_no_remunerativo, include_currency=False))
    c.drawString(coordinates['dupl_concepto_titles_x_ap'], coordinates['starting_y_totales'],
                 float_to_format_currency(totales_retenciones, include_currency=False))
    c.setFont(FONT_FAMILY_BOLD, FONT_SIZE_MAIN)
    c.drawString(coordinates['dupl_concepto_titles_x_ap'] - 0.5 * cm, coordinates['starting_y_totales_neto'],
                 float_to_format_currency(neto_liquidacion, include_currency=False))
    c.setFont(FONT_FAMILY, FONT_SIZE_BODY)
    c.drawString(coordinates['company_x'], coordinates['neto_letras_y'], f"Son: {neto_en_letras}")
    c.drawString(coordinates['dupl_company_x'], coordinates['neto_letras_y'], f"Son: {neto_en_letras}")

    # End of Totales ----------------------------------------------------------------------------

    # Pie de página -------------------------------------------------------------------------------
    pie_linea_1_y = coordinates['pie_de_pagina_y']
    pie_linea_2_y = coordinates['pie_de_pagina_y'] - base_line_between
    pie_linea_3_y = coordinates['pie_de_pagina_y'] - base_line_between * 2

    pie_pagina_column_2 = coordinates['pie_de_pagina_x'] + coordinates['pie_de_pagina_width'] / 2
    dupl_pie_pagina_column_2 = coordinates['dupl_pie_de_pagina_x'] + coordinates['pie_de_pagina_width'] / 2

    # Original
    forma_pago = info_recibo['relaciones_bancarias'][legajo]['forma_pago']
    numero_cuenta = info_recibo['relaciones_bancarias'][legajo]['numero_cuenta']

    pagado_como = "Abonado en Efectivo"
    if forma_pago.lower()[:2] == 'ch':
        pagado_como = "Abonado con Cheque"

    if numero_cuenta:
        pagado_como = f"Depositado en Cuenta Nº {numero_cuenta}"

    c.drawString(coordinates['pie_de_pagina_x'], pie_linea_1_y, f'Fecha de Pago: {info_recibo["fecha_pago"]}')
    c.drawString(coordinates['pie_de_pagina_x'], pie_linea_2_y, f'Lugar: {lugar_trabajo}')
    c.drawString(coordinates['pie_de_pagina_x'], pie_linea_3_y, pagado_como)

    c.drawString(pie_pagina_column_2, pie_linea_1_y, "Último Depósito Aportes y Contribuciones")
    c.line(
        x1=pie_pagina_column_2,
        y1=pie_linea_1_y - 0.12 * cm,
        x2=pie_pagina_column_2 + coordinates['pie_de_pagina_width'] * 0.41,
        y2=pie_linea_1_y - 0.12 * cm
    )
    if info_recibo['ultimo_pago_ss']['id']:
        periodo_ss = f'{nombre_mes(int(info_recibo["ultimo_pago_ss"]["mes"]))} {info_recibo["ultimo_pago_ss"]["anio"]}'
        fecha_pago_ss = formatted_date_str(info_recibo['ultimo_pago_ss']['fecha_pago'])
        banco_ss = info_recibo['ultimo_pago_ss']['banco']
        c.drawString(pie_pagina_column_2, pie_linea_2_y, f'Período: {periodo_ss} - {fecha_pago_ss}')
        c.drawString(pie_pagina_column_2, pie_linea_3_y, f'Banco: {banco_ss}')

    # Duplicate
    recibi_conforme_text = "Recibi de conformidad importe neto y copia de este recibo, dejando constancia que "
    recibi_conforme_text += "a la fecha no se me adeudan haberes, licencias ni horas extras."

    draw_text_with_max_width(
        canvas=c,
        text=recibi_conforme_text,
        max_width=coordinates['pie_de_pagina_width'] * 0.47,
        # max_width=20,
        x=coordinates['dupl_pie_de_pagina_x'],
        y=pie_linea_1_y,
    )
    c.drawString(dupl_pie_pagina_column_2, pie_linea_1_y, "Último Depósito Aportes y Contribuciones")
    c.line(
        x1=dupl_pie_pagina_column_2,
        y1=pie_linea_1_y - 0.12 * cm,
        x2=dupl_pie_pagina_column_2 + coordinates['pie_de_pagina_width'] * 0.41,
        y2=pie_linea_1_y - 0.12 * cm
    )
    if info_recibo['ultimo_pago_ss']['id']:
        periodo_ss = f'{nombre_mes(int(info_recibo["ultimo_pago_ss"]["mes"]))} {info_recibo["ultimo_pago_ss"]["anio"]}'
        fecha_pago_ss = formatted_date_str(info_recibo['ultimo_pago_ss']['fecha_pago'])
        banco_ss = info_recibo['ultimo_pago_ss']['banco']
        c.drawString(dupl_pie_pagina_column_2, pie_linea_2_y, f'Período: {periodo_ss} - {fecha_pago_ss}')
        c.drawString(dupl_pie_pagina_column_2, pie_linea_3_y, f'Banco: {banco_ss}')

    # Fin de Pie de página ------------------------------------------------------------------------
