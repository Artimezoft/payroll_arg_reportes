from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from py_arg_reports.config import config_constants

FONT_FAMILY = config_constants['FONT_FAMILY']
FONT_FAMILY_BOLD = config_constants['FONT_FAMILY_BOLD']
FONT_SIZE_MAIN = config_constants['FONT_SIZE_MAIN']
FONT_SIZE_BODY = config_constants['FONT_SIZE_BODY']


def my_base_recibo(c: Canvas) -> dict:
    """ Base of payslip, it set all the lines and texts that are common to all payslips
    """
    tot_y = 21 * cm
    tot_x = 29.7 * cm
    half_of_width = tot_x / 2 - 0.4 * cm
    mid_margin = 0 * cm
    margin_between_lines = 0.2 * cm
    def_radius = 7

    resp = {
        'tot_y': tot_y,
        'tot_x': tot_x,
        'half_of_width': half_of_width,
        'mid_margin': mid_margin,
        'margin_between_lines': margin_between_lines,
    }

    # Aprox Margins
    # margin_x = 1.5 * cm
    margin_y = 1.2 * cm

    # Defining heights
    available_height = tot_y - 2 * margin_y
    company_name_height = available_height * 0.09 - margin_between_lines
    employee_info_height = available_height * 0.16 - margin_between_lines
    conceptos_height = available_height * 0.65 - margin_between_lines
    total_height = available_height * 0.1 - margin_between_lines

    c.translate(cm, cm)

    # Base Rectangles
    # Company Info --------------------------------------------------------------------------------
    gray_value = 0.93
    c.setFillColorRGB(gray_value, gray_value, gray_value)

    company_name_width = 10.5 * cm
    starting_y = tot_y - margin_y - company_name_height
    resp['company_info_y'] = starting_y
    resp['company_info_height'] = company_name_height
    resp['duplicate_x'] = half_of_width + mid_margin

    c.roundRect(0, starting_y, company_name_width, company_name_height, radius=def_radius, stroke=1, fill=1)
    c.roundRect(
        half_of_width + mid_margin,
        starting_y,
        company_name_width,
        company_name_height,
        radius=def_radius,
        stroke=1,
        fill=1
    )

    # Liquidacion Info --------------------------------------------------------------------------------
    original_x = company_name_width + 0.1 * cm
    duplicate_x = half_of_width + mid_margin + company_name_width + 0.1 * cm
    liquidacion_info_width = 3 * cm
    resp['liquidacion_info_x'] = original_x
    resp['liquidacion_info_width'] = liquidacion_info_width
    resp['liquidacion_info_x_duplicate'] = duplicate_x

    c.roundRect(original_x, starting_y, liquidacion_info_width, company_name_height, radius=def_radius, stroke=1, fill=0)
    c.roundRect(duplicate_x, starting_y, liquidacion_info_width, company_name_height, radius=def_radius, stroke=1, fill=0)
    # lines in the half
    c.line(
        original_x,
        starting_y + company_name_height / 2,
        original_x + liquidacion_info_width,
        starting_y + company_name_height / 2
    )
    c.line(
        duplicate_x,
        starting_y + company_name_height / 2,
        duplicate_x + liquidacion_info_width,
        starting_y + company_name_height / 2
    )

    # Employee Info --------------------------------------------------------------------------------
    starting_y -= employee_info_height + margin_between_lines
    employee_info_width = liquidacion_info_width + company_name_width + 0.1 * cm
    resp['employee_info_y'] = starting_y
    resp['employee_info_height'] = employee_info_height
    resp['employee_info_width'] = employee_info_width

    c.roundRect(0, starting_y, employee_info_width, employee_info_height, radius=def_radius, stroke=1, fill=0)
    c.roundRect(
        half_of_width + mid_margin,
        starting_y,
        employee_info_width,
        employee_info_height,
        radius=def_radius,
        stroke=1,
        fill=0
    )

    # Conceptos --------------------------------------------------------------------------------
    starting_y -= conceptos_height + margin_between_lines
    conceptos_width = employee_info_width
    resp['conceptos_y'] = starting_y + conceptos_height
    resp['conceptos_height'] = conceptos_height

    c.roundRect(0, starting_y, conceptos_width, conceptos_height, radius=def_radius, stroke=1, fill=0)
    c.roundRect(half_of_width + mid_margin, starting_y, conceptos_width, conceptos_height, radius=def_radius, stroke=1, fill=0)

    # Títulos de conceptos
    c.setFont(FONT_FAMILY_BOLD, FONT_SIZE_MAIN)
    c.setFillColorRGB(0, 0, 0)

    conceptos_titles_y = resp['conceptos_y'] - 0.3 * cm
    concepto_titles_x_cant = conceptos_width * 0.50
    concepto_titles_x_rem = conceptos_width * 0.60
    concepto_titles_x_nr = conceptos_width * 0.73
    concepto_titles_x_ap = conceptos_width * 0.86

    dupl_concepto_titles_x_cant = half_of_width + mid_margin + concepto_titles_x_cant
    dupl_concepto_titles_x_rem = half_of_width + mid_margin + concepto_titles_x_rem
    dupl_concepto_titles_x_nr = half_of_width + mid_margin + concepto_titles_x_nr
    dupl_concepto_titles_x_ap = half_of_width + mid_margin + concepto_titles_x_ap

    resp['conceptos_titles_y'] = conceptos_titles_y
    resp['concepto_titles_x_cant'] = concepto_titles_x_cant
    resp['concepto_titles_x_rem'] = concepto_titles_x_rem
    resp['concepto_titles_x_nr'] = concepto_titles_x_nr
    resp['concepto_titles_x_ap'] = concepto_titles_x_ap
    resp['dupl_concepto_titles_x_cant'] = dupl_concepto_titles_x_cant
    resp['dupl_concepto_titles_x_rem'] = dupl_concepto_titles_x_rem
    resp['dupl_concepto_titles_x_nr'] = dupl_concepto_titles_x_nr
    resp['dupl_concepto_titles_x_ap'] = dupl_concepto_titles_x_ap

    c.drawString(0.5 * cm, conceptos_titles_y, "Conceptos")
    c.drawString(concepto_titles_x_cant + 0.1 * cm, conceptos_titles_y, "Cant.")
    c.drawString(concepto_titles_x_rem + 0.2 * cm, conceptos_titles_y, "Remun.")
    c.drawString(concepto_titles_x_nr + 0.2 * cm, conceptos_titles_y, "No Rem.")
    c.drawString(concepto_titles_x_ap + 0.2 * cm, conceptos_titles_y, "Retenc.")

    c.drawString(half_of_width + mid_margin + 0.5 * cm, conceptos_titles_y, "Conceptos")
    c.drawString(dupl_concepto_titles_x_cant + 0.1 * cm, conceptos_titles_y, "Cant.")
    c.drawString(dupl_concepto_titles_x_rem + 0.2 * cm, conceptos_titles_y, "Remun.")
    c.drawString(dupl_concepto_titles_x_nr + 0.2 * cm, conceptos_titles_y, "No Rem.")
    c.drawString(dupl_concepto_titles_x_ap + 0.2 * cm, conceptos_titles_y, "Retenc.")

    # Linea para totales
    starting_y_totales = starting_y + conceptos_height * 0.15
    starting_y_totales_texto = starting_y_totales - 0.5 * cm
    starting_y_totales_neto = starting_y + 0.5 * cm

    resp['starting_y_totales'] = starting_y_totales_texto
    resp['starting_y_totales_neto'] = starting_y_totales_neto

    c.line(
        0,
        starting_y_totales,
        conceptos_width,
        starting_y_totales,
    )
    c.drawString(0.5 * cm, starting_y_totales_texto, "Totales:")
    c.drawString(conceptos_width - 5 * cm, starting_y_totales_neto, "Neto a Pagar:")

    c.line(
        half_of_width + mid_margin,
        starting_y_totales,
        half_of_width + mid_margin + conceptos_width,
        starting_y_totales,
    )
    c.drawString(half_of_width + mid_margin + 0.5 * cm, starting_y_totales_texto, "Totales:")
    c.drawString(half_of_width + mid_margin + conceptos_width - 5 * cm, starting_y_totales_neto, "Neto a Pagar:")

    # Total --------------------------------------------------------------------------------
    # Original
    starting_y -= total_height + margin_between_lines + 0.45 * cm
    firma_width = 5 * cm
    rect_height = total_height * 1.1

    resp['pie_pagina_y'] = starting_y + rect_height - 0.45 * cm
    resp['pie_pagina_height'] = rect_height
    resp['pie_pagina_width'] = conceptos_width

    c.roundRect(
        0,
        starting_y,
        conceptos_width,
        rect_height,
        radius=def_radius,
        stroke=1,
        fill=0
    )

    c.line(
        conceptos_width / 2,
        starting_y,
        conceptos_width / 2,
        starting_y + rect_height,
    )

    c.line(
        half_of_width / 2 - firma_width / 2 - 1 * cm,
        0,
        half_of_width / 2 + firma_width / 2 - 1 * cm,
        0,
    )
    c.setFont(FONT_FAMILY, FONT_SIZE_BODY)

    c.drawString(half_of_width / 2 - firma_width / 2, -0.5 * cm, "Firma del empleador")

    # Duplicate
    c.roundRect(
        half_of_width + mid_margin,
        starting_y,
        conceptos_width,
        rect_height,
        radius=def_radius,
        stroke=1,
        fill=0
    )

    c.line(
        half_of_width + mid_margin + conceptos_width / 2,
        starting_y,
        half_of_width + mid_margin + conceptos_width / 2,
        starting_y + rect_height,
    )

    c.line(
        half_of_width + mid_margin + 1 * cm,
        0,
        half_of_width + mid_margin + firma_width + 1 * cm,
        0,
    )
    c.drawString(half_of_width + mid_margin + 2 * cm, -0.5 * cm, "Firma del empleado")

    resp['canvas'] = c

    return resp
