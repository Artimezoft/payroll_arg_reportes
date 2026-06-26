import io
import unittest

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from py_arg_reports.config import config_constants
from py_arg_reports.reporters.recibo_sueldo.modelos.recibo_3 import FormatoRecibo3


class TestRecibo3LayoutConfig(unittest.TestCase):
    def _build_layout(self):
        buffer = io.BytesIO()
        canvas = Canvas(buffer, pagesize=A4)
        return FormatoRecibo3(canvas)

    def test_recibo_3_coordinates_contract(self):
        layout = self._build_layout()
        layout.draw_background()
        coords = layout.get_coordinates()

        required_keys = {
            "company_info_y",
            "company_info_height",
            "liquidacion_info_x",
            "liquidacion_info_width",
            "employee_info_y",
            "employee_info_height",
            "employee_info_width",
            "conceptos_y",
            "conceptos_height",
            "conceptos_titles_y",
            "concepto_titles_x_cant",
            "concepto_titles_x_rem",
            "concepto_titles_x_nr",
            "concepto_titles_x_ap",
            "starting_y_totales",
            "starting_y_totales_neto",
            "contribuciones_y",
            "contribuciones_height",
            "contribuciones_titles_y",
            "pie_pagina_y",
            "pie_pagina_width",
            "pie_pagina_height",
            "margin_x",
            "has_duplicate",
        }
        self.assertTrue(required_keys.issubset(set(coords.keys())))
        self.assertFalse(coords["has_duplicate"])

    def test_recibo_3_allows_global_overrides_from_config(self):
        original = dict(config_constants.get("RECIBO_3_LAYOUT", {}))
        try:
            config_constants["RECIBO_3_LAYOUT"] = {"margin_x_cm": 1.2, "company_width_ratio": 0.7}

            layout = self._build_layout()
            layout.draw_background()
            coords = layout.get_coordinates()

            self.assertAlmostEqual(coords["margin_x"], 1.2 * cm, places=3)
        finally:
            config_constants["RECIBO_3_LAYOUT"] = original


if __name__ == "__main__":
    unittest.main()
