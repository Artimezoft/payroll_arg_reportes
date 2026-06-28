import pytest
import json
from pathlib import Path
from py_arg_reports.reporters.acreditaciones.santander import AcreditacionSantander


class TestAcreditacionSantander:
    """ Testing para Acreditaciones Santander """

    def setup_method(self):
        self.samples_folder = Path('py_arg_reports/reporters/acreditaciones/data')
        self.temp_folder = self.samples_folder / 'temp'
        # Crear la carpeta temporal
        self.temp_folder.mkdir(exist_ok=True)

    def test_acreditacion_santander_no_data(self):
        data = {}
        with pytest.raises(ValueError):
            AcreditacionSantander(data=data)

    def test_acreditacion_santander_no_empresa(self):
        data = {
            'liquidacion': {
                'total_pago': '1000.00',
            }
        }
        with pytest.raises(ValueError):
            AcreditacionSantander(data=data)

    def test_bad_codigo_de_pago(self):
        file_data = self.samples_folder / 'sample_santander_bad_codigo_de_pago.json'
        data = json.load(open(file_data))
        with pytest.raises(ValueError) as e:
            AcreditacionSantander(data)
        expected = 'No hay un codigo_forma_pago'
        error = str(e.value)
        assert expected in error

    def test_acreditacion_santander_ok(self):
        file_data = self.samples_folder / 'sample-santander.json'
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
        assert len(result_lines) == 1 + len(acreditacion.empleados) + 1
        header = result_lines[0]
        self._test_header(header)
        trailer = result_lines[-1]
        self._test_trailer(trailer, acreditacion)
        detalles = result_lines[1:-2]
        for det in detalles:
            self._test_detalle(det)

    def _test_header(self, header):
        # El header empieza con H
        assert header[0] == 'H'
        assert len(header) == 650
        cuit = header[1:12]
        # assert all numbers
        assert cuit.isdigit()
        assert header[12] == '0'
        cod_productos = ['011', '013']
        cod_prod = header[13:16]
        assert cod_prod in cod_productos
        nro_acuerdo = header[16:18]
        nro_acuerdos_validos = ['88']
        assert nro_acuerdo in nro_acuerdos_validos
        cod_canal = header[18:21]
        assert cod_canal == '007'
        nro_envio = header[21:26]
        assert nro_envio == '00001'
        reservado = header[26:31]
        assert reservado == '00000'
        reservado = header[31:38]
        assert reservado == ' ' * 7
        validacion_cuil = header[38]
        assert validacion_cuil == 'S'
        reservado = header[39:650]
        assert reservado == ' ' * 611

    def _test_trailer(self, trailer, acreditacion):
        # El trailer empieza con T
        assert trailer[0] == 'T'
        assert len(trailer) == 650
        # 15 ceros (reservado)
        assert trailer[1:16] == '0' * 15
        # 15 digitos, pago total
        total_pago = trailer[16:31]
        assert total_pago.isdigit()
        # 7 digitos para la cantidad de registros
        cant_registros = trailer[31:38]
        assert cant_registros.isdigit()
        can_registros_num = int(cant_registros)
        assert can_registros_num == len(acreditacion.empleados)
        # 612 ceros
        assert trailer[38:650] == '0' * 612

    def _test_detalle(self, det):
        """ Cada detalle es un empleado """
        # El detalle empieza con D
        assert det[0] == 'D'
        assert len(det) == 650
        assert det[1] == ' '
        monedas = ['0', '2', '8']
        moneda = det[2]
        assert moneda in monedas
        # legajo = det[3:18]  # No hay validacion
        assert det[18:20] == 'RC'
        anio = det[20:24]
        assert det[20:22] == '20'
        assert anio.isdigit(), anio + det[18:30]
        mes = det[24:26]
        assert mes.isdigit()
        mes_num = int(mes)
        assert 1 <= mes_num <= 12
        # ceros hasta llegar a los 15 caracteres
        assert det[26:35] == '0' * 9
        assert det[35:39] == '0000'
        nombre = det[39:69]
        assert nombre.strip()
        direccion = det[69:120]
        assert direccion.strip()
        assert det[120:125] == '00000'
        assert det[125:129] == ' ' * 4
        assert det[129:212] == '0' * 83
        assert det[212:223] == ' ' * 11
        cuil = det[223:234]
        assert cuil.isdigit()
        assert det[234:396] == ' ' * 162
        assert det[396] == 'N'
        assert det[397:401] == '0054'
        codigo_cbu = det[401:427]
        assert codigo_cbu.isdigit()
        # el cbu empieza con cero
        assert codigo_cbu[0] == '0'
        # Luego tiene 3 ceros fijos en la posicion 9, 10 y 11
        assert codigo_cbu[8:11] == '000'
        assert det[427:435] == '0' * 8
        # fecha pago AAAAMMDD
        fecha_pago = det[435:443]
        assert fecha_pago.isdigit()
        assert fecha_pago[0:2] == '20'
        mes = int(fecha_pago[4:6])
        assert 1 <= mes <= 12
        dia = int(fecha_pago[6:8])
        assert 1 <= dia <= 31
        # importe de pago, 15 digitos
        importe = det[443:458]
        assert importe.isdigit()
        cod_pagos_validos = ['50', '52', '57']
        cod_pago = det[458:460]
        assert cod_pago in cod_pagos_validos
        assert det[460:463] == ' ' * 3
        # 11 ceros (reservado)
        assert det[463:474] == '0' * 11
        # 3 espacios (reservado)
        assert det[474:477] == ' ' * 3
        # 11 ceros (reservado)
        assert det[477:488] == '0' * 11
        # 3 espacios (reservado)
        assert det[488:491] == ' ' * 3
        # 11 ceros (reservado)
        assert det[491:502] == '0' * 11
        # 3 espacios (reservado)
        assert det[502:505] == ' ' * 3
        # 25 ceros (reservado)
        assert det[505:530] == '0' * 25
        # Un espacio (reservado)
        assert det[530] == ' '
        # 17 ceros (reservado)
        assert det[531:548] == '0' * 17
        # 102 espacios
        assert det[548:650] == ' ' * 102
