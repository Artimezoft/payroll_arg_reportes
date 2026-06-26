from reportlab.lib.units import cm

from py_arg_reports.reporters.recibo_sueldo.base import FormatoReciboSueldo
from py_arg_reports.config import config_constants

FONT_FAMILY = config_constants["FONT_FAMILY"]
FONT_FAMILY_BOLD = config_constants["FONT_FAMILY_BOLD"]
FONT_SIZE_MAIN = config_constants["FONT_SIZE_MAIN"]
FONT_SIZE_BODY = config_constants["FONT_SIZE_BODY"]


class FormatoRecibo3(FormatoReciboSueldo):
    """Proof-of-concept reusable layout implementation.

    This class keeps the same coordinate contract expected by
    ReciboDownloader.get_coordinates_for_recibo so the rendering pipeline can
    remain stable while new layouts become class-based and reusable.
    """

    def draw_background(self):
        c = self.canvas

        tot_x = 19 * cm
        tot_y = 29.7 * cm
        margin_between_lines = 0.2 * cm
        def_radius = 7
        margin_x = 0.4 * cm

        self.coordinates = {
            "tot_x": tot_x,
            "tot_y": tot_y,
            "margin_between_lines": margin_between_lines,
            "margin_x": margin_x,
            "has_duplicate": False,
        }

        margin_y = 0.3 * cm

        available_height = tot_y - 2 * margin_y
        available_width = tot_x - 2 * margin_x

        company_name_height = available_height * 0.07 - margin_between_lines
        employee_info_height = available_height * 0.13 - margin_between_lines
        conceptos_height = available_height * 0.58 - margin_between_lines
        contribuciones_height = available_height * 0.11 - margin_between_lines
        total_height = available_height * 0.11 - margin_between_lines

        c.translate(cm, cm)

        gray_value = 0.93
        c.setFillColorRGB(gray_value, gray_value, gray_value)

        company_name_width = available_width * 0.78
        starting_y = tot_y - margin_y - company_name_height - 0.9 * cm

        self.coordinates["company_info_y"] = starting_y
        self.coordinates["company_info_height"] = company_name_height

        c.roundRect(
            margin_x,
            starting_y,
            company_name_width,
            company_name_height,
            radius=def_radius,
            stroke=1,
            fill=1,
        )

        # Liquidacion Info ---------------------------------------------------------------
        original_x = margin_x + company_name_width + 0.1 * cm
        liquidacion_info_width = available_width - company_name_width - 0.1 * cm
        self.coordinates["liquidacion_info_x"] = original_x
        self.coordinates["liquidacion_info_width"] = liquidacion_info_width

        c.roundRect(
            original_x,
            starting_y,
            liquidacion_info_width,
            company_name_height,
            radius=def_radius,
            stroke=1,
            fill=0,
        )
        c.line(
            original_x,
            starting_y + company_name_height / 2,
            original_x + liquidacion_info_width,
            starting_y + company_name_height / 2,
        )

        # Employee Info -----------------------------------------------------------------
        starting_y -= employee_info_height + margin_between_lines
        employee_info_width = available_width
        self.coordinates["employee_info_y"] = starting_y
        self.coordinates["employee_info_height"] = employee_info_height
        self.coordinates["employee_info_width"] = employee_info_width

        c.roundRect(
            margin_x,
            starting_y,
            employee_info_width,
            employee_info_height,
            radius=def_radius,
            stroke=1,
            fill=0,
        )

        # Conceptos ---------------------------------------------------------------------
        starting_y -= conceptos_height + margin_between_lines
        conceptos_width = employee_info_width
        self.coordinates["conceptos_y"] = starting_y + conceptos_height
        self.coordinates["conceptos_height"] = conceptos_height

        c.roundRect(
            margin_x,
            starting_y,
            conceptos_width,
            conceptos_height,
            radius=def_radius,
            stroke=1,
            fill=0,
        )

        c.setFont(FONT_FAMILY_BOLD, FONT_SIZE_MAIN)
        c.setFillColorRGB(0, 0, 0)

        conceptos_titles_y = self.coordinates["conceptos_y"] - 0.3 * cm
        concepto_titles_x_cant = margin_x + conceptos_width * 0.56
        concepto_titles_x_rem = margin_x + conceptos_width * 0.68
        concepto_titles_x_nr = margin_x + conceptos_width * 0.80
        concepto_titles_x_ap = margin_x + conceptos_width * 0.91

        self.coordinates["conceptos_titles_y"] = conceptos_titles_y
        self.coordinates["concepto_titles_x_cant"] = concepto_titles_x_cant
        self.coordinates["concepto_titles_x_rem"] = concepto_titles_x_rem
        self.coordinates["concepto_titles_x_nr"] = concepto_titles_x_nr
        self.coordinates["concepto_titles_x_ap"] = concepto_titles_x_ap

        c.drawString(margin_x + 0.5 * cm, conceptos_titles_y, "Conceptos")
        c.drawString(concepto_titles_x_cant + 0.1 * cm, conceptos_titles_y, "Cant.")
        c.drawString(concepto_titles_x_rem + 0.2 * cm, conceptos_titles_y, "Remun.")
        c.drawString(concepto_titles_x_nr + 0.2 * cm, conceptos_titles_y, "No Rem.")
        c.drawString(concepto_titles_x_ap + 0.2 * cm, conceptos_titles_y, "Retenc.")

        # Linea para totales -------------------------------------------------------------
        starting_y_totales = starting_y + conceptos_height * 0.15
        starting_y_totales_texto = starting_y_totales - 0.5 * cm
        starting_y_totales_neto = starting_y + 0.6 * cm

        self.coordinates["starting_y_totales"] = starting_y_totales_texto
        self.coordinates["starting_y_totales_neto"] = starting_y_totales_neto

        c.line(
            margin_x,
            starting_y_totales,
            margin_x + conceptos_width,
            starting_y_totales,
        )
        c.drawString(margin_x + 0.5 * cm, starting_y_totales_texto, "Totales:")
        c.drawString(margin_x + conceptos_width - 5.2 * cm, starting_y_totales_neto, "Neto a Pagar:")

        # Contribuciones ----------------------------------------------------------------
        starting_y -= contribuciones_height + margin_between_lines
        contribuciones_width = employee_info_width
        self.coordinates["contribuciones_y"] = starting_y + contribuciones_height
        self.coordinates["contribuciones_height"] = contribuciones_height

        c.roundRect(
            margin_x,
            starting_y,
            contribuciones_width,
            contribuciones_height,
            radius=def_radius,
            stroke=1,
            fill=0,
        )

        c.setFont(FONT_FAMILY_BOLD, FONT_SIZE_MAIN)
        c.setFillColorRGB(0, 0, 0)

        contribuciones_titles_y = self.coordinates["contribuciones_y"] - 0.3 * cm
        self.coordinates["contribuciones_titles_y"] = contribuciones_titles_y

        c.drawString(margin_x + 0.5 * cm, contribuciones_titles_y, "Contribuciones")

        # Pie / firma area ---------------------------------------------------------------
        starting_y -= total_height + margin_between_lines + 0.25 * cm
        rect_height = total_height * 1.1

        pie_pagina_y = starting_y + rect_height - 0.45 * cm
        self.coordinates["pie_pagina_y"] = pie_pagina_y
        self.coordinates["pie_pagina_height"] = rect_height
        self.coordinates["pie_pagina_width"] = conceptos_width

        c.roundRect(
            margin_x,
            starting_y,
            conceptos_width,
            rect_height,
            radius=def_radius,
            stroke=1,
            fill=0,
        )

        c.line(
            margin_x + conceptos_width / 2 + 2 * cm,
            starting_y,
            margin_x + conceptos_width / 2 + 2 * cm,
            starting_y + rect_height,
        )

        c.setFont(FONT_FAMILY, FONT_SIZE_BODY)
        self.coordinates["canvas"] = c
