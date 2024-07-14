import json
import os
import tempfile
import unittest

from py_arg_reports.reporters.libro_sueldo_digital.reporter import genera_txt_lsd


class TestGeneracionLSD(unittest.TestCase):
    """ Testing para Generación Libro Sueldos Digital
    """
    @classmethod
    def setUpClass(cls):
        # Specify the path where the temporary folder should be created
        temp_folder_path = './tests/temp/'
        # Create a temporary folder for testing in the specified path
        cls.temp_folder = tempfile.mkdtemp(dir=temp_folder_path)
        if cls.temp_folder[-1] != '/':
            cls.temp_folder += '/'

        with open('./py_arg_reports/test_cases/lsd-info-1l.json', 'r') as f:
            cls.json_data_1l = json.load(f)
        with open('./py_arg_reports/test_cases/lsd-info-2l.json', 'r') as f:
            cls.json_data_2l = json.load(f)
        with open('./py_arg_reports/test_cases/lsd-info-missing_conceptos.json', 'r') as f:
            cls.missing_conceptos = json.load(f)
        with open('./py_arg_reports/test_cases/lsd-info-missing_empleados.json', 'r') as f:
            cls.missing_empleados = json.load(f)
        with open('./py_arg_reports/test_cases/lsd-info-missing_info931.json', 'r') as f:
            cls.missing_info931 = json.load(f)
        with open('./py_arg_reports/test_cases/lsd-info-missing_info931_campos.json', 'r') as f:
            cls.missing_info931_campos = json.load(f)
        cls.empty_json = {}
        cls.keys_missing_json = {
            "periodo": "2024-03-01",
            "empresa": "GLADYS LUCAS HERNAN",
            "cuit": "20123456780",
            "cantidad_liquidaciones": 1
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

    def test_descarga_lsd_1(self):
        """ Prueba de la generacion de txt de Libro Sueldos Digital con 1 liquidacion
        """
        resp_descarga = genera_txt_lsd(
            json_data=self.json_data_1l,
            output_path=self.temp_folder,
            filename='txt_lsd_prueba',
        )

        self.assertEqual(resp_descarga, (True, None))
        # Le agrega el "_1" por ser liquidacion 1
        full_path = self.temp_folder + 'txt_lsd_prueba_1.txt'
        print("full_path: ", full_path)

        # Check if the file exists
        self.assertTrue(os.path.exists(full_path))

        # Check the number of lines in the txt file
        with open(self.temp_folder + 'txt_lsd_prueba_1.txt', 'r') as file:
            # Recorro las líneas del archivo, los 2 primeros caracteres de cada línea son el tipo de registro
            # Deben tener este largo:
            # '01': Datos referenciales del envío -> Largo 35
            # '02': Datos referenciales de la Liquidación de SyJ del trabajador -> Largo 115
            # '03': Detalle de los conceptos de sueldo liquidados al trabajador -> Largo 51
            # '04': Datos del trabajador para el calculo de la DJ F931 -> Largo 370
            # '05': Datos de Eventuales -> Largo 65
            lines = file.readlines()
            # Tienen que ser 5 líneas porque tiene:
            # 1 línea de tipo 01
            # 1 línea de tipo 02
            # 13 línea de tipo 03
            # 1 línea de tipo 04
            self.assertEqual(len(lines), 16)

        for line in lines:
            # le remuevo el salto de carro si tiene
            line = line.replace('\n', '')

            if line[:2] == '01':
                self.assertEqual(len(line), 35)
            elif line[:2] == '02':
                self.assertEqual(len(line), 115)
            elif line[:2] == '03':
                self.assertEqual(len(line), 51)
            elif line[:2] == '04':
                self.assertEqual(len(line), 370)
            elif line[:2] == '05':
                self.assertEqual(len(line), 65)

    def test_descarga_empty_json(self):
        """ Prueba la descarga del archivo para un json vacío
        """
        resp_descarga = genera_txt_lsd(
            json_data=self.empty_json,
            output_path=self.temp_folder,
            filename='txt_lsd_prueba',
        )

        self.assertEqual(resp_descarga, (False, 'No se puede generar el txt para Libro Sueldo Digital, no hay datos'))
        full_path = self.temp_folder + 'txt_lsd_prueba_1.txt'

        # Check if the file not exists
        self.assertFalse(os.path.exists(full_path))

    def test_key_missing_conceptos(self):
        """ Prueba la descarga del archivo para un json con conceptos faltantes
        """
        resp_descarga = genera_txt_lsd(
            json_data=self.missing_conceptos,
            output_path=self.temp_folder,
            filename='txt_lsd_prueba',
        )

        self.assertEqual(resp_descarga, (False, 'Falta la clave conceptos_liquidados en el diccionario de empleados'))

    def test_key_missing_infof931(self):
        """ Prueba la descarga del archivo para un json con info_f931 faltante
        """
        resp_descarga = genera_txt_lsd(
            json_data=self.missing_info931,
            output_path=self.temp_folder,
            filename='txt_lsd_prueba',
        )

        self.assertEqual(resp_descarga, (False, 'Falta la clave info_f931 en el diccionario de empleados'))

    def test_key_missing_infof931_campos(self):
        """ Prueba la descarga del archivo para un json con algunos campos de info_f931 faltantes
        """
        resp_descarga = genera_txt_lsd(
            json_data=self.missing_info931_campos,
            output_path=self.temp_folder,
            filename='txt_lsd_prueba',
        )

        self.assertEqual(resp_descarga, (False, 'Falta el campo convencionado en el diccionario de info_931'))

    def test_broken_json(self):
        """ Prueba la descarga del archivo para un json roto
        """
        resp_descarga = genera_txt_lsd(
            json_data=self.keys_missing_json,
            output_path=self.temp_folder,
            filename='txt_lsd_prueba',
        )

        self.assertEqual(resp_descarga, (False, 'No se puede generar el txt, dato esencial liquidaciones no encontrado'))

    def test_key_missing_empleados(self):
        """ Prueba la descarga del archivo para un json con empleados faltantes
        """
        resp_descarga = genera_txt_lsd(
            json_data=self.missing_empleados,
            output_path=self.temp_folder,
            filename='txt_lsd_prueba',
        )

        expected_resp = 'No se puede generar el txt, dato esencial empleados_liquidados no encontrado en liquidaciones'
        self.assertEqual(resp_descarga, (False, expected_resp))


if __name__ == '__main__':
    unittest.main()
