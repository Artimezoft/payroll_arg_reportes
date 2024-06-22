from py_arg_reports.reporters.acreditaciones import AcreditacionesHeadDetailTrailerFile
from py_arg_reports.tools.txt import fixed_width_str, str_dec_num_to_no_dec_sep


class AcreditacionSantander(AcreditacionesHeadDetailTrailerFile):
    """ Un archivo para el banco Santander """

    def generate_header(self):
        """ Generar el header """
        ret = "H"
        ret += self.empresa.get('cuit')
        ret += "0"
        ret += "011"  # Codigo de producto 011 es haberes y 013 es honorarios
        ret += self.get_nro_de_acuerdo()  # Nro de acuerdo (asignado por el banco)
        ret += "007"  # Codigo de canal 007 Online Banking Cash Management 005 Diskette
        ret += "00001"  # Numero de envio: suponemos que se manda un solo envio por dia
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
        ret += fixed_width_str(legajo_str, 15, align='right')
        # 5 Tipo de comprobante, fijo en RC
        ret += 'RC'
        # 6 Numero de comprobante Num, 15, AAAAMM rellenado con ceros a la izquierda
        anio = self.liquidacion.get('periodo_anio')
        mes = self.liquidacion.get('periodo_mes')
        periodo = f'{anio}{mes:02}'
        ret += f'{periodo:015}'
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
        ret += self.get_codigo_cbu(empleado)
        # 19 Reservado para usos futuros, Num, 8
        ret += '0' * 8
        # 20 Fecha de pago, Num, 8, AAAAMMDD
        anio = int(self.liquidacion.get('fecha_pago_anio'))
        mes = int(self.liquidacion.get('fecha_pago_mes'))
        dia = int(self.liquidacion.get('fecha_pago_dia'))
        full_dia = f'{anio}{mes:02}{dia:02}'
        ret += full_dia
        # 21 Import del pago, Num, 15, (13 enteros y 2 decimales sin separador)
        # Nuestro importe viene en string aun siedo un numero para que no se pierda precision
        parte_entera, parte_decimal = str_dec_num_to_no_dec_sep(empleado.get('importe_pago'))
        # asegurarse que la parte entera tiene 13 digitos y la parte decimal tiene 2 digitos con format string
        numero_sin_separa = f'{parte_entera:013}{parte_decimal:02}'
        ret += numero_sin_separa
        # 22 Codigo de forma de pago, Num, 2, 50=Acredit Santander, 52=SNP (otros bancos), 57=CCI (Otros bancos)
        ret += self.get_codigo_forma_pago()
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

    def get_codigo_cbu(self, empleado):
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
            EN RESUMEN. ES UN CBU COMUN QUE EMPIEZA CON UN 0 Y METE ADEMAS 3 CEROS FIJOS ANTES DEL SEGUNDO BLOQUE
            Al parecer tenian miedo de que se les acaben los numeros de cuenta.
            Ejemplo real Santander
            072 0469 6 8 8 00003516919 0

             Wikipedia: https://es.wikipedia.org/wiki/Clave_Bancaria_Uniforme
                La CBU está compuesta por 22 dígitos, separados en dos bloques. El primer bloque tiene un número de entidad
                de 3 dígitos, un número de sucursal de 4 dígitos y un dígito verificador. El segundo bloque tiene un número
                de 13 dígitos que identifica la cuenta dentro de la entidad y la sucursal, más un dígito verificador.
                [
                    XXX BANCO (ver tabla)
                    YYYY SUCURSAL
                    D DÍGITO VERIFICADOR
                    +
                    CTA[13] 13 digitos para la cuenta dentro del banco y sucursal
                    D DÍGITO VERIFICADOR
                ]
                Para el número de entidad de 3 dígitos que compone el primer bloque, debe verificarse el código de banco con
                la siguiente tabla de bancos
        """
        cbu = empleado.get('cbu')
        return '0' + cbu[0:9] + '000' + cbu[9:23]

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

    def get_nro_de_acuerdo(self):
        """ Devuelve un numero de acuerdo.
            Este es un codigo de dos digitos que se asigna por el banco.
            Se lo tenes que pedir a tu ejecutivo de cuenta.
        """

        return self.extras.get('nro_de_acuerdo', '00')

    def get_codigo_forma_pago(self):
        """ Devuelve el codigo de forma de pago """
        cfp = self.extras.get('codigo_forma_pago', '50')
        if cfp not in ['50', '52', '57']:
            raise ValueError('Código de forma de pago inválido')
        return cfp
