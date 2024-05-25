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
        self._test_trailer(trailer, acreditacion)
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

    def _test_trailer(self, trailer, acreditacion):
        # El trailer empieza con T
        self.assertEqual(trailer[0], 'T')
        self.assertEqual(len(trailer), 650)
        # 15 ceros (reservado)
        self.assertEqual(trailer[1:16], '0' * 15)
        # 15 digitos, pago total
        total_pago = trailer[16:31]
        self.assertTrue(total_pago.isdigit())
        # 7 digitos para la cantidad de registros
        cant_registros = trailer[31:38]
        self.assertTrue(cant_registros.isdigit())
        can_registros_num = int(cant_registros)
        self.assertEqual(can_registros_num, len(acreditacion.empleados))
        # 612 ceros
        self.assertEqual(trailer[38:650], '0' * 612)

    def _test_detalle(self, det):
        """ Cada detalle es un empleado """
        # El detalle empieza con D
        self.assertEqual(det[0], 'D')
        self.assertEqual(len(det), 650)
        self.assertEqual(det[1], ' ')
        monedas = ['0', '2', '8']
        moneda = det[2]
        self.assertIn(moneda, monedas)
        # legajo = det[3:18]  # No hay validacion
        self.assertEqual(det[18:20], 'RC')
        anio = det[20:24]
        self.assertEqual(det[20:22], '20')
        self.assertTrue(anio.isdigit(), anio + det[18:30])
        mes = det[24:26]
        self.assertTrue(mes.isdigit())
        mes_num = int(mes)
        self.assertTrue(1 <= mes_num <= 12)
        # ceros hasta llegar a los 15 caracteres
        self.assertEqual(det[26:35], '0' * 9)
        self.assertEqual(det[35:39], '0000')
        nombre = det[39:69]
        self.assertTrue(nombre.strip())
        direccion = det[69:120]
        self.assertTrue(direccion.strip())
        self.assertEqual(det[120:125], '00000')
        self.assertEqual(det[125:129], ' ' * 4)
        self.assertEqual(det[129:212], '0' * 83)
        self.assertEqual(det[212:223], ' ' * 11)
        cuil = det[223:234]
        self.assertTrue(cuil.isdigit())
        self.assertEqual(det[234:396], ' ' * 162)
        self.assertEqual(det[396], 'N')
        self.assertEqual(det[397:401], '0054')
        codigo_cbu = det[401:427]
        self.assertTrue(codigo_cbu.isdigit())
        # el cbu empieza con cero
        self.assertEqual(codigo_cbu[0], '0')
        # Luego tiene 3 ceros fijos en la posicion 9, 10 y 11
        self.assertEqual(codigo_cbu[8:11], '000')
        self.assertEqual(det[427:435], '0' * 8)
        # fecha pago AAAAMMDD
        fecha_pago = det[435:443]
        self.assertTrue(fecha_pago.isdigit())
        self.assertEqual(fecha_pago[0:2], '20')
        mes = int(fecha_pago[4:6])
        self.assertTrue(1 <= mes <= 12)
        dia = int(fecha_pago[6:8])
        self.assertTrue(1 <= dia <= 31)
        # importe de pago, 15 digitos
        importe = det[443:458]
        self.assertTrue(importe.isdigit())
        cod_pagos_validos = ['50', '52', '57']
        cod_pago = det[458:460]
        self.assertIn(cod_pago, cod_pagos_validos)
        self.assertEqual(det[460:463], ' ' * 3)
        # 11 ceros (reservado)
        self.assertEqual(det[463:474], '0' * 11)
        # 3 espacios (reservado)
        self.assertEqual(det[474:477], ' ' * 3)
        # 11 ceros (reservado)
        self.assertEqual(det[477:488], '0' * 11)
        # 3 espacios (reservado)
        self.assertEqual(det[488:491], ' ' * 3)
        # 11 ceros (reservado)
        self.assertEqual(det[491:502], '0' * 11)
        # 3 espacios (reservado)
        self.assertEqual(det[502:505], ' ' * 3)
        # 25 ceros (reservado)
        self.assertEqual(det[505:530], '0' * 25)
        # Un espacio (reservado)
        self.assertEqual(det[530], ' ')
        # 17 ceros (reservado)
        self.assertEqual(det[531:548], '0' * 17)
        # 102 espacios
        self.assertEqual(det[548:650], ' ' * 102)
