from pathlib import Path
import json
import unittest
# from PyPDF2 import PdfReader
from py_arg_reports.reporters.libro_sueldo import descargar_libro


class TestLibroSueldo(unittest.TestCase):
    """ Testing para Descargar libro sueldo """

    def setUp(self):
        self.samples_folder = 'py_arg_reports/reporters/libro_sueldo/samples'
        self.temp_folder = Path(self.samples_folder) / 'temp/'

    def test_descarga_recibo_1(self):
        """ Prueba la descarga del archivo """
        sample = 'samples-recibo-info.json'
        sample_path = Path(self.samples_folder) / sample
        json_data = json.load(open(sample_path))
        ok, error = descargar_libro(
            json_data=json_data,
            output_path=self.temp_folder,
            filename='pdf1',
        )

        self.assertIsNone(error)
        self.assertTrue(ok)
        expected_path = Path(self.temp_folder) / 'pdf1.pdf'

        # Check if the file exists
        self.assertTrue(expected_path.exists())

        # # Check the number of pages in the PDF file
        # with open(full_path, 'rb') as file:
        #     # pdf_reader = PyPDF2.PdfFileReader(f)
        #     pdf = PdfReader(file)
        #     num_sheets = len(pdf.pages)

        # self.assertEqual(num_sheets, 3)
