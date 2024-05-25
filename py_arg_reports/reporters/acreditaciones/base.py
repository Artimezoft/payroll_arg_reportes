class AcreditacionFile:
    """ Un archivo para un banco (generico) """

    def __init__(self, data):
        self.data = data

        self.empresa = None
        self.empleados = []
        # Datos de esta liquidacion
        self.liquidacion = None
        # Cargar los datos
        self.load_data()
        # Incluye los headers el archivo final?
        self.include_headers = True

    def load_data(self):
        """ Cargar los datos
            Para todos los bancos tenemos los mismos datos de origen
        """
        # validar que tenemos una lista de empleados
        empleados = self.data.get('empleados')
        if not isinstance(empleados, list):
            raise ValueError('No hay una lista de empleados')
        for empleado in empleados:
            empleado = self.validate_empleado(empleado)
            self.empleados.append(empleado)
        # validar que tenemos un diccionario con los datos de la empresa
        empresa = self.data.get('empresa')
        if not isinstance(empresa, dict):
            raise ValueError('No hay un diccionario con los datos de la empresa')
        self.empresa = self.validate_empresa(empresa)
        liquidacion = self.data.get('liquidacion')
        if not isinstance(liquidacion, dict):
            raise ValueError('No hay un diccionario con los datos de la liquidacion')
        # validar el total de pagos
        if not liquidacion.get('total_pago'):
            raise ValueError('No hay un total de pagos en la liquidacion')
        total_from_empleados = sum(
            [
                float(empleado.get('importe_pago'))
                for empleado in empleados
            ]
        )
        total_pago = float(liquidacion.get('total_pago'))
        if abs(total_from_empleados - total_pago) > 1:
            error = (
                'El total de pagos no coincide con la suma de los pagos de los empleados'
                f'{total_from_empleados} != {total_pago}'
            )
            raise ValueError(error)
        self.liquidacion = liquidacion

    def validate_empleado(self, empleado):
        """ Validar los datos de un empleado """
        if not empleado.get('nombre'):
            raise ValueError('No hay un nombre de empleado')
        if not empleado.get('apellido'):
            raise ValueError('No hay un apellido de empleado')
        if not empleado.get('cuil'):
            raise ValueError('No hay un cuil de empleado')
        return empleado

    def validate_empresa(self, empresa):
        """ Validar los datos de la empresa """
        if not empresa.get('razon_social'):
            raise ValueError('No hay un nombre de empresa')
        if not empresa.get('cuit'):
            raise ValueError('No hay un cuit de empresa')
        return empresa

    def generate_file(self, path):
        """ Generar el archivo """
        raise NotImplementedError


class AcreditacionesHeadDetailTrailerFile(AcreditacionFile):
    """Este es un archivo de texto con
        Header  -> generate_header
        Detalle -> generate_detalle_empleado
        Trailer -> generate_trailer
    """

    def generate_file(self, path):
        """ Generar el archivo
            Devuelve un booleano y un mensaje de error (si hay)
        """
        f = open(path, 'w')
        header = self.generate_header()
        f.write(header)
        for empleado in self.empleados:
            detalle_empleado = self.generate_detalle_empleado(empleado)
            f.write(detalle_empleado)
        trailer = self.generate_trailer()
        f.write(trailer)
        f.close()
        return True, None
