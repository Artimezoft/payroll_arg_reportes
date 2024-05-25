from py_arg_reports.reporters.acreditaciones import AcreditacionesHeadDetailTrailerFile
from py_arg_reports.tools.txt import fixed_width_str, str_dec_num_to_no_dec_sep


class AcreditacionSantander(AcreditacionesHeadDetailTrailerFile):
    """ Un archivo para el banco Santander """

    def generate_header(self):
        """ Generar el header """
        ret = "H"
        ret += self.empresa.get('cuit')
        ret += "0"
        ret += "011"  # 011 es haberes y 013 es honorarios
        ret += "00"  # TODO de donde saco esto?
        ret += "007"  # 007 Online Banking Cash Management 005 Diskette
        ret += "00001"  # suponemos que se manda un solo envio por dia
        ret += "00000"  # Reservado para usos futuros
        ret += " " * 7  # Reservado para usos futuros
        ret += "S"  # Validacion CUIL
        ret += " " * 611  # Reservado para usos futuros
        return ret

    def generate_detalle_empleado(self, empleado):
        """ Generar el empleado """
        # 1 Tipo de registro = D detalle
        ret = 'D'
        # 2 Reservado para usos futuros, Alf, 1 = espacio
        ret += ' '
        # 3 Moneda 0=pesos, 2=dolares, 8=bimonetaira
        ret += '0'
        # 4 Numero del beneficiario (interno empresa) Alf
        # 15 caracters fijos
        legajo_str = str(empleado.get('legajo'))
        ret += fixed_width_str(legajo_str, 15)
        # 5 Tipo de comprobante, fijo en RC
        ret += 'RC'
        # 6 Numero de comprobante Num, 15, AAAAMM rellenado con ceros a la izquierda
        anio = str(self.liquidacion.get('periodo_anio'))
        mes = str(self.liquidacion.get('periodo_mes'))
        ret += anio + fixed_width_str(mes, 2, align='right', fill_with='0')
        # 7 Reservado para usos futuros, num, 4
        ret += '0000'
        # 8 Nombre del beneficiario, Alf, 30
        nombre_completo = empleado.get('nombre') + ' ' + empleado.get('apellido')
        ret += fixed_width_str(nombre_completo, 30)
        # 9 Direccion del beneficiario, Alf, 51
        ret += fixed_width_str(empleado.get('direccion'), 51)
        # 10 Reservado para usos futuros, Num, 5
        ret += '00000'
        # 11 Reservado para usos futuros, Alf, 4
        ret += ' ' * 4
        # 12 Reservado para usos futuros, Num, 83
        ret += '0' * 83
        # 13 Reservado para usos futuros, Alf, 11
        ret += ' ' * 11
        # 14 CUIL del beneficiario, Num, 11
        ret += empleado.get('cuil')
        # 15 Reservado para usos futuros, Alf, 162
        ret += ' ' * 162
        # 16 Marca de Agrup de beneficiarios, fijo="N"
        ret += 'N'
        # 17 Pais, fijo 0054
        ret += '0054'
        # TODO esto no esta listo
        # 18 CBU beneficiario. 26 caracteres, Diferente para Santender u otros
        ret += self.get_codigo_cbu()
        # 19 Reservado para usos futuros, Num, 8
        ret += '0' * 8
        # 20 Fecha de pago, Num, 8, AAAAMMDD
        anio = str(self.liquidacion.get('fecha_pago_anio'))
        mes = str(self.liquidacion.get('fecha_pago_mes'))
        dia = str(self.liquidacion.get('fecha_pago_dia'))
        ret += anio + fixed_width_str(
            mes, 2, align='right', fill_with='0'
        ) + fixed_width_str(
            dia, 2, align='right', fill_with='0'
        )
        # 21 Import del pago, Num, 15, (13 enteros y 2 decimales sin separador)
        # Nuestro importe viene en string aun siedo un numero para que no se pierda precision
        parte_entera, parte_decimal = str_dec_num_to_no_dec_sep(empleado.get('importe_pago'))
        # asegurarse que la parte entera tiene 13 digitos y la parte decimal tiene 2 digitos con format string
        numero_sin_separa = f'{parte_entera:013}{parte_decimal:02}'
        ret += numero_sin_separa
        # 22 Codigo de forma de pago, Num, 2, 50=Acredit Santander, 52=SNP (otros bancos), 57=CCI (Otros bancos)
        ret += '50'  # TODO averiguar esto
        # 23 Reservado para usos futuros, Alf, 3
        ret += ' ' * 3
        # 24 Reservado para usos futuros, Num, 11
        ret += '0' * 11
        # 25 Reservado para usos futuros, Alf, 3
        ret += ' ' * 3
        # 26 Reservado para usos futuros, Num, 11
        ret += '0' * 11
        # 27 Reservado para usos futuros, Alf, 3
        ret += ' ' * 3
        # 28 Reservado para usos futuros, Num, 11
        ret += '0' * 11
        # 29 Reservado para usos futuros, Alf, 3
        ret += ' ' * 3
        # 30 Reservado para usos futuros, Num, 25
        ret += '0' * 25
        # 31 Reservado para usos futuros, Alf, 1
        ret += ' '
        # 32 Reservado para usos futuros, Num, 17
        ret += '0' * 17
        # 33 Reservado para usos futuros, Alf, 102
        ret += ' ' * 102
        return ret

    def get_codigo_cbu(self):
        """ Devuelve el CBU en formato especifico
            18 CBU beneficiario. 26 caracteres, Diferente para Santender u otros
            Santander:
             - Num(1) fijo 0
             - Num(3) Codigo de banco = 072 VER /acreditaciones/data/bancos.json
             - Num(4) Numero de sucursal
             - Num(1) Digito verificador Bloque 1
             - Num(3) Fijo 000
             - Num(1) Tipo de cuenta: 2=cta cte, 3=caja ahorro, 8=infinity
             - Num(1) Moneda: 0=pesos, 8=bimonetaria
             - Num(11) Numero de cuenta
             - Num(1) Digito verificador Bloque 2
            Otros bancos:
             - Num(1) fijo 0
             - Num(8) Bloque 1
             - Num(3) fijo 000
             - Num(14) Bloque 2
        """
        return '9' * 26

    def generate_trailer(self):
        """ Generar el trailer """
        ret = 'T'  # 1 Tipo de registro = T trailer
        # 2 Reservado para usos futuros, Num, 15
        ret += '0' * 15
        # 3 Importe total del pago Num, 15, (13 enteros y 2 decimales sin separador)
        parte_entera, parte_decimal = str_dec_num_to_no_dec_sep(self.liquidacion.get('total_pago'))
        # asegurarse que la parte entera tiene 13 digitos y la parte decimal tiene 2 digitos con format string
        numero_sin_separa = f'{parte_entera:013}{parte_decimal:02}'
        ret += numero_sin_separa
        # 4 Cantidad de registros Num, 7
        total_empleados = len(self.empleados)
        ret += f'{total_empleados:07}'
        # 5 Reservado para usos futuros, Num, 612
        ret += '0' * 612
        return ret
