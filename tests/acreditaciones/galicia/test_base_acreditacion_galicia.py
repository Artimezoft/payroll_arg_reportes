import json
import unittest
from pathlib import Path
import openpyxl
from py_arg_reports.reporters.acreditaciones.galicia import AcreditacionGalicia


class TestAcreditacionGalicia(unittest.TestCase):
    """ Testing para Acreditaciones Santander """

    def setUp(self):
        self.samples_folder = Path('py_arg_reports/reporters/acreditaciones/data')
        self.temp_folder = self.samples_folder / 'temp'
        # Crear la carpeta temporal
        self.temp_folder.mkdir(exist_ok=True)

    def test_acreditacion_galicia_no_data(self):
        data = {}
        with self.assertRaises(ValueError):
            AcreditacionGalicia(data=data)

    def test_acreditacion_galicia_no_nro_cuenta(self):
        file_data = self.samples_folder / 'sample-galicia-missing-nro-cuenta.json'
        data = json.load(open(file_data))
        with self.assertRaises(ValueError) as e:
            AcreditacionGalicia(data)
        expected = 'No hay un nro_cuenta de empleado'
        self.assertIn(expected, str(e.exception))

    def test_acreditacion_galicia_no_pago(self):
        file_data = self.samples_folder / 'sample-galicia-missing-importe-pago.json'
        data = json.load(open(file_data))
        with self.assertRaises(ValueError) as e:
            AcreditacionGalicia(data)
        expected = 'No hay un importe_pago de empleado'
        self.assertIn(expected, str(e.exception))

    def test_acreditacion_galicia_ok(self):
        file_data = self.samples_folder / 'sample-galicia.json'
        data = json.load(open(file_data))
        acreditacion = AcreditacionGalicia(data)
        destination = self.temp_folder / 'galicia.xlsx'
        process, error = acreditacion.generate_file(destination)
        self.assertTrue(process, error)
        # test results excel file
        self.assertTrue(destination.exists())
        # test the content of the excel file
        expected = [
            ['Cuenta', 'Nombre', 'Importe', 'Concepto'],
            ['00209023941002', 'Juan Perez', 1236119.04, 1],
            ['00209023941003', 'Pedro Argento', 5216108.17, 1],
        ]

        wb = openpyxl.load_workbook(destination)
        ws = wb.active
        for row, values in enumerate(expected):
            for col, value in enumerate(values):
                self.assertEqual(ws.cell(row=row+1, column=col+1).value, value)
        wb.close()
