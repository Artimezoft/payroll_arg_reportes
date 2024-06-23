class AcreditacionFile:
    """ Un archivo para un banco (generico)
        El init le permite a las clases que heredan definir muchas cosas.
        Las funciones estan separadas para que cada banco pueda sobreescribir lo que necesite.
    """

    def __init__(
            self, data,
            empresa_required=True,
            liquidacion_required=True,
            include_headers=True,
            empleados_require=['nombre', 'apellido', 'cuil'],
            empresa_require=['razon_social', 'cuit'],
            liquidacion_require=[],
            extras_require=[],
    ):
        self.data = data

        self.empresa = None
        self.empleados = []
        # Datos de esta liquidacion
        self.liquidacion = None
        # Extras que cada banco puede requerir
        self.extras = {}
        # Incluye los headers el archivo final?
        self.include_headers = include_headers

        # Definir que es obligatorio, cada clase lo elige
        # Empresa es requerida? Por ejemplo para Galicia no es requerida
        self.empresa_required = empresa_required
        self.liquidacion_required = liquidacion_required

        # Cada objeto puede definir que campos son requeridos
        self.empleados_require = empleados_require
        self.empresa_require = empresa_require
        self.liquidacion_require = liquidacion_require
        self.extras_require = extras_require

        self.load_data()

    def load_data(self):
        """ Cargar los datos """
        self.load_empleados(require=self.empleados_require)
        self.load_empresa(require=self.empresa_require)
        self.load_liquidacion(require=self.liquidacion_require)
        self.load_extras(require=self.extras_require)

    def load_empleados(self, require=[]):
        """ Cargar los datos de los empleados """
        # validar que tenemos una lista de empleados
        empleados = self.data.get('empleados')
        if not isinstance(empleados, list):
            raise ValueError('No hay una lista de empleados')
        for empleado in empleados:
            empleado = self.validate_empleado(empleado, require)
            self.empleados.append(empleado)

    def validate_empleado(self, empleado, require=[]):
        """ Validar los datos de un empleado """
        for field in require:
            if not empleado.get(field):
                raise ValueError(f'No hay un {field} de empleado')
        return empleado

    def load_empresa(self, require=[]):
        """ Cargar los datos de la empresa """
        empresa = self.data.get('empresa')
        if self.empresa_required and not isinstance(empresa, dict):
            raise ValueError('No hay un diccionario con los datos de la empresa')
        self.empresa = self.validar_empresa(empresa, require) if empresa else None

    def load_liquidacion(self, require=[]):
        """ Cargar los datos de la liquidacion """
        liquidacion = self.data.get('liquidacion')
        self.validar_liquidacion(liquidacion, require)
        self.liquidacion = liquidacion

    def validar_liquidacion(self, liquidacion, require=[]):
        """ Si hay una, validar la liquidacion """
        if not liquidacion:
            if self.liquidacion_required and not isinstance(liquidacion, dict):
                raise ValueError('No hay un diccionario con los datos de la liquidacion')
            self.liquidacion = None
            return

        # validar el total de pagos (si existe)
        if liquidacion.get('total_pago'):
            self.validar_total_pago(liquidacion)

        # ver si hay campos requeridos
        for field in require:
            if not liquidacion.get(field):
                raise ValueError(f'No hay un {field} de liquidacion')

        self.liquidacion = liquidacion

    def validar_total_pago(self, liquidacion):
        """ Ver que el total de pagos sea el mismo a la suma de los pagos de los empleados """
        total_from_empleados = sum(
            [
                float(empleado.get('importe_pago'))
                for empleado in self.empleados
            ]
        )
        # Si total_pago es "0" entonces lo calculo solo sin validar
        if liquidacion.get('total_pago') == "0":
            liquidacion['total_pago'] = str(total_from_empleados)
        else:
            total_pago = float(liquidacion.get('total_pago'))
            if abs(total_from_empleados - total_pago) > 5:
                error = (
                    'El total de pagos no coincide con la suma de los pagos de los empleados'
                    f'{total_from_empleados} != {total_pago}'
                )
                raise ValueError(error)

    def validar_empresa(self, empresa, require=[]):
        """ Validar los datos de la empresa """
        for field in require:
            if not empresa.get(field):
                raise ValueError(f'No hay un {field} de empresa')
        return empresa

    def load_extras(self, require=[]):
        """ Cargar los extras """
        self.extras = self.data.get('extras', {})
        for field in require:
            if not self.extras.get(field):
                raise ValueError(f'No hay un {field} de extras: {self.extras}')

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
        f.write('\n')
        for empleado in self.empleados:
            detalle_empleado = self.generate_detalle_empleado(empleado)
            f.write(detalle_empleado)
            f.write('\n')
        trailer = self.generate_trailer()
        f.write(trailer)
        f.close()
        return True, None
