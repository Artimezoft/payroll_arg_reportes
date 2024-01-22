import json
import os
import tempfile
import unittest

from PyPDF2 import PdfReader

from reporters.recibo_sueldo import descargar_recibo


class TestDownloadRecibo(unittest.TestCase):
    """ Testing para Descargar Recibos
    """
    @classmethod
    def setUpClass(cls):
        # Specify the path where the temporary folder should be created
        current_path = os.getcwd()
        temp_folder_path = current_path
        # Create a temporary folder for testing in the specified path
        cls.temp_folder = tempfile.mkdtemp(dir=temp_folder_path)
        if cls.temp_folder[-1] != '/':
            cls.temp_folder += '/'

        with open(f'{current_path}/src/test_cases/liquidacion_completa.json', 'r') as f:
            cls.long_json = json.load(f)

        with open(f'{current_path}/src/test_cases/liquidacion_corta.json', 'r') as f:
            cls.short_json = json.load(f)

    def setUp(self):
        self.empty_json = {}
        self.no_results_json = {'results': []}
        self.key_missing_json = {'results': [{
            'empleado': 'Juan',
            'empresa': 'Empresa',
            'conceptos_liquidados': 'Conceptos',
            'liquidacion': 'Liquidacion',
            }]}

    @classmethod
    def tearDownClass(cls):
        # Clean up: Delete the temporary folder and its contents
        if os.path.exists(cls.temp_folder):
            for root, dirs, files in os.walk(cls.temp_folder, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            os.rmdir(cls.temp_folder)

    def test_descarga_recibo_1(self):
        """ Prueba la descarga del archivo
        """
        resp_descarga = descargar_recibo(
            json_data=self.short_json,
            output_path=self.temp_folder,
            filename='recibo_prueba_1',
        )

        self.assertEqual(resp_descarga, '')
        full_path = self.temp_folder + 'recibo_prueba_1.pdf'

        # Check if the file exists
        self.assertTrue(os.path.exists(full_path))

        # Check the number of pages in the PDF file
        with open(full_path, 'rb') as file:
            # pdf_reader = PyPDF2.PdfFileReader(f)
            pdf = PdfReader(file)
            num_sheets = len(pdf.pages)

        self.assertEqual(num_sheets, 3)

    def test_descarga_recibo_2(self):
        """ Prueba la descarga del archivo full
        """
        resp_descarga = descargar_recibo(
            json_data=self.long_json,
            output_path=self.temp_folder,
            filename='recibo_prueba_2',
        )

        self.assertEqual(resp_descarga, '')
        full_path = self.temp_folder + 'recibo_prueba_2.pdf'

        # Check if the file exists
        self.assertTrue(os.path.exists(full_path))

        # Check the number of pages in the PDF file
        with open(self.temp_folder + 'recibo_prueba_2.pdf', 'rb') as file:
            # pdf_reader = PyPDF2.PdfFileReader(f)
            pdf = PdfReader(file)
            num_sheets = len(pdf.pages)

        self.assertEqual(num_sheets, 25)

    def test_descarga_empty_json(self):
        """ Prueba la descarga del archivo para un json vacío
        """
        resp_descarga = descargar_recibo(
            json_data=self.empty_json,
            output_path=self.temp_folder,
            filename='recibo_prueba_3',
        )

        self.assertEqual(resp_descarga, 'No se puede descargar el recibo, no hay datos')

    def test_no_results_json(self):
        """ Prueba la descarga del archivo para un json sin resultados
        """
        resp_descarga = descargar_recibo(
            json_data=self.no_results_json,
            output_path=self.temp_folder,
            filename='recibo_prueba_4',
        )

        self.assertEqual(resp_descarga, 'No se puede descargar el recibo, faltan datos')

    def test_key_missing_json(self):
        """ Prueba la descarga del archivo para un json sin la key 'results'
        """
        resp_descarga = descargar_recibo(
            json_data=self.key_missing_json,
            output_path=self.temp_folder,
            filename='recibo_prueba_5',
        )

        self.assertEqual(resp_descarga, 'No se puede descargar el recibo, no se observa totales_liquidacion en los datos')


if __name__ == '__main__':
    unittest.main()
