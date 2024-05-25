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
        # test results file
        f = open(destination)
        result_text = f.read()
        f.close()
        result_lines = result_text.split('\n')
        # Header + Detalles + Trailer
        self.assertEqual(len(result_lines), 1 + len(acreditacion.empleados) + 1)
        header = result_lines[0]
        self._test_header(header)
        trailer = result_lines[-1]
        self._test_trailer(trailer)
        detalles = result_lines[1:-2]
        for det in detalles:
            self._test_detalle(det)

    def _test_header(self, header):
        # El header empieza con H
        self.assertEqual(header[0], 'H')
        self.assertEqual(len(header), 650)
        cuit = header[1:12]
        # assert all numbers
        self.assertTrue(cuit.isdigit())
        self.assertEqual(header[12], '0')
        cod_productos = ['011', '013']
        cod_prod = header[13:16]
        self.assertIn(cod_prod, cod_productos)
        nro_acuerdo = header[16:18]
        nro_acuerdos_validos = ['00']  # TODO de donde saco esto?
        self.assertIn(nro_acuerdo, nro_acuerdos_validos)
        cod_canal = header[18:21]
        self.assertEqual(cod_canal, '007')
        nro_envio = header[21:26]
        self.assertEqual(nro_envio, '00001')
        reservado = header[26:31]
        self.assertEqual(reservado, '00000')
        reservado = header[31:38]
        self.assertEqual(reservado, ' ' * 7)
        validacion_cuil = header[38]
        self.assertEqual(validacion_cuil, 'S')
        reservado = header[39:650]
        self.assertEqual(reservado, ' ' * 611)

    def _test_trailer(self, trailer):
        # El trailer empieza con T
        self.assertEqual(trailer[0], 'T')
        self.assertEqual(len(trailer), 650)

    def _test_detalle(self, det):
        """ Cada detalle es un empleado """
        # El detalle empieza con D
        self.assertEqual(det[0], 'D')
        self.assertEqual(len(det), 650)
