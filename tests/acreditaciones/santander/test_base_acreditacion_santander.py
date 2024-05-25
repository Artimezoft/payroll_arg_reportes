import json
import unittest
from pathlib import Path
from py_arg_reports.reporters.acreditaciones.santander import AcreditacionSantander


class TestAcreditacionSantander(unittest.TestCase):
    """ Testing para Acreditaciones Santander """

    def setUp(self):
        self.samples_folder = Path('py_arg_reports/reporters/acreditaciones/data')
        self.temp_folder = self.samples_folder / 'temp'
        # Crear la carpeta temporal
        self.temp_folder.mkdir(exist_ok=True)

    def test_acreditacion_santander_no_data(self):
        data = {}
        with self.assertRaises(ValueError):
            AcreditacionSantander(data=data)

    def test_acreditacion_santander_no_empresa(self):
        data = {
            'liquidacion': {
                'total_pago': '1000.00',
            }
        }
        with self.assertRaises(ValueError):
            AcreditacionSantander(data=data)

    def test_acreditacion_santander_ok(self):
        file_data = self.samples_folder / 'sample.json'
        data = json.load(open(file_data))
        acreditacion = AcreditacionSantander(data)
        destination = self.temp_folder / 'santa.txt'
        process, _ = acreditacion.generate_file(destination)
        assert process
