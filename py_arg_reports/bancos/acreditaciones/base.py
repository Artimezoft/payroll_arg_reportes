class AcreditacionFile:
    """ Un archivo para un banco (generico) """

    def __init__(self, data):
        self.data = data
        self.load_data()
        self.empresa = None
        self.empleados = None
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
        if not empresa.get('nombre'):
            raise ValueError('No hay un nombre de empresa')
        if not empresa.get('cuit'):
            raise ValueError('No hay un cuit de empresa')
        return empresa

    def generate_file(self, path):
        """ Generar el archivo """
        raise NotImplementedError
