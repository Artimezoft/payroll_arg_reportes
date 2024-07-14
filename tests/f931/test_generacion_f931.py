import json
import os
import tempfile
import unittest

from py_arg_reports.reporters.f931.reporter import genera_txt_f931


class TestGeneracionF931(unittest.TestCase):
    """ Testing para Generación F931
    """
    @classmethod
    def setUpClass(cls):
        # Specify the path where the temporary folder should be created
        temp_folder_path = './tests/temp/'
        # Create a temporary folder for testing in the specified path
        cls.temp_folder = tempfile.mkdtemp(dir=temp_folder_path)
        if cls.temp_folder[-1] != '/':
            cls.temp_folder += '/'

        with open('./py_arg_reports/test_cases/f931-info.json', 'r') as f:
            cls.json_data = json.load(f)
        cls.empty_json = {}
        cls.key_missing_json = {
            "cuit": "30704552744",
            "periodo": "2024-04-01",
            "txt_empleados": [
                {
                    "cuil": "23223334441",
                    "nombre_completo": "GOMEZ, JUAN",
                    "conyuge": 0,
                    "hijos": 0,
                }
            ],
        }

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

    def test_descarga_f931_1(self):
        """ Prueba de la generacion de txt de f931
        """
        resp_descarga = genera_txt_f931(
            json_data=self.json_data,
            output_path=self.temp_folder,
            filename='txt_f931_prueba_1',
        )

        self.assertEqual(resp_descarga, (True, None))
        full_path = self.temp_folder + 'txt_f931_prueba_1.txt'

        # Check if the file exists
        self.assertTrue(os.path.exists(full_path))

        # Check the number of lines in the txt file
        with open(self.temp_folder + 'txt_f931_prueba_1.txt', 'r') as file:
            lines = file.readlines()
            num_lines = len(lines)
            largo_linea = len(lines[0]) if lines else 0

        # La línea debe tener 500 caracteres (incluyendo el salto de línea)
        # y el archivo 2 líneas por 2 empleados
        self.assertEqual(largo_linea, 500)
        self.assertEqual(num_lines, 2)

    def test_descarga_empty_json(self):
        """ Prueba la descarga del archivo para un json vacío
        """
        resp_descarga = genera_txt_f931(
            json_data=self.empty_json,
            output_path=self.temp_folder,
            filename='txt_f931_prueba_2',
        )

        self.assertEqual(resp_descarga, (False, 'No se puede generar el txt para el F931, no hay datos'))

        full_path = self.temp_folder + 'txt_f931_prueba_2.txt'

        # Check if the file not exists
        self.assertFalse(os.path.exists(full_path))

    def test_key_missing_json(self):
        """ Prueba la descarga del archivo para un json con datos faltantes
        """
        resp_descarga = genera_txt_f931(
            json_data=self.key_missing_json,
            output_path=self.temp_folder,
            filename='txt_f931_prueba_3',
        )

        self.assertEqual(resp_descarga, (False, 'El campo situacion no fue encontrado en los datos'))


if __name__ == '__main__':
    unittest.main()
