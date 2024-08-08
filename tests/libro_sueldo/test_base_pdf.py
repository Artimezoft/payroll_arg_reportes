from pathlib import Path
import json
import unittest
from PyPDF2 import PdfReader
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

        # Check content
        f = open(str(expected_path), 'rb')
        # Check the number of pages in the PDF file
        pdf = PdfReader(f)
        pages = len(pdf.pages)
        self.assertEqual(pages, 1)

        # Probar que el contenido del archivo sea el esperado
        page = pdf.pages[0]
        page_1_text = page.extract_text()
        print("page_1_text", page_1_text)
        expected = [
            'Empresa de Prueba',
            'Calle de Prueba 123, 10, Formosa',
            'Actividad de Prueba',
            'No Remunerativos',
            # Agregue cosas y ya no se el total 'Neto a cobrar $ 329.181,77'
        ]
        for text in expected:
            self.assertIn(text, page_1_text)
