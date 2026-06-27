import json

from reportlab.pdfgen.canvas import Canvas

from py_arg_reports.reporters.recibo_sueldo.base import (
    ReciboDownloader,
    ReciboPartBounds,
    get_info_final_for_recibo,
    get_recibo_info,
)
from py_arg_reports.reporters.recibo_sueldo.layouts import get_layout_for_version


class TestReciboParts:
    @classmethod
    def setup_class(cls):
        with open('./py_arg_reports/test_cases/liquidacion_corta.json', 'r', encoding='utf-8') as f:
            cls.short_json = json.load(f)

    def _build_recibo(self, base_version=3):
        layout = get_layout_for_version(base_version)
        c = Canvas('tests/temp/recibo_parts_test.pdf', pagesize=layout.pagesize)
        info = get_info_final_for_recibo(get_recibo_info(self.short_json))
        my_recibo_info = layout.draw_background(c)
        coordinates = ReciboDownloader.get_coordinates_for_recibo(my_recibo_info)

        return info, c, coordinates

    def test_parts_have_expected_order(self):
        info, c, coordinates = self._build_recibo(base_version=3)
        legajo = info['legajos'][0]

        from py_arg_reports.reporters.recibo_sueldo.base import ReciboSueldo

        recibo = ReciboSueldo(c, coordinates, info, legajo, base_version=3)
        names = [part.name for part in recibo.get_parts()]

        assert names == ['title', 'employee', 'contribuciones', 'conceptos', 'composition_salario']

    def test_parts_have_expected_order_for_legacy(self):
        info, c, coordinates = self._build_recibo(base_version=1)
        legajo = info['legajos'][0]

        from py_arg_reports.reporters.recibo_sueldo.base import ReciboSueldo

        recibo = ReciboSueldo(c, coordinates, info, legajo, base_version=1)
        names = [part.name for part in recibo.get_parts()]

        assert names == ['title', 'employee', 'contribuciones', 'conceptos', 'signature']

    def test_each_part_has_valid_bounds(self):
        info, c, coordinates = self._build_recibo(base_version=3)
        legajo = info['legajos'][0]

        from py_arg_reports.reporters.recibo_sueldo.base import ReciboSueldo

        recibo = ReciboSueldo(c, coordinates, info, legajo, base_version=3)

        for part in recibo.get_parts():
            bounds = part.bounds
            assert isinstance(bounds, ReciboPartBounds)
            assert bounds.from_x < bounds.to_x
            assert bounds.from_y < bounds.to_y
