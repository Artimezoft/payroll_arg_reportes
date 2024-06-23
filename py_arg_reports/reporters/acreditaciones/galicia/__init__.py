import logging
from py_arg_reports.reporters.acreditaciones import AcreditacionFile
from py_arg_reports.reporters.descarga_excel import descarga_excel


log = logging.getLogger(__name__)


class AcreditacionGalicia(AcreditacionFile):
    """ Un archivo para el banco Santander """
    def __init__(self, data):
        super().__init__(
            data,
            empresa_required=False,
            liquidacion_required=False,
            empleados_require=['nombre', 'apellido', 'nro_cuenta', 'importe_pago'],
        )
        # Galicia es muy simple, posiblemente toma los datos desde el sistema del banco
        # Aqui solo pasamos un Excel con los datos de los empleados

    def load_data(self):
        """ Cargar solo los datos de empleados """
        self.load_empleados(require=self.empleados_require)

    def generate_file(self, path):
        """ Generar el archivo Excel que espera Galicia """
        data = {
            'headers': {
                'header1': {
                    'name': 'Cuenta',
                    'format': {'font_name': 'Arial', 'font_size': 12}
                },
                'header2': {
                    'name': 'Nombre',
                    'format': {'font_name': 'Arial', 'font_size': 12}
                },
                'header3': {
                    'name': 'Importe',
                    'format': {'num_format': '0.00', 'font_name': 'Arial', 'font_size': 12},
                    'is_number': True,
                },
                'header4': {
                    'name': 'Concepto',
                    'format': {'num_format': '0', 'font_name': 'Arial', 'font_size': 12},
                    'is_number': True,
                },
            },
            'data': []
        }

        for empleado in self.empleados:
            nombre = empleado.get('nombre', '')
            apellido = empleado.get('apellido', '')
            nro_cuenta = empleado.get('nro_cuenta')
            importe_pago = empleado.get('importe_pago')
            if isinstance(importe_pago, str):
                importe_pago = float(importe_pago)
            emp_dict = {
                'header1': nro_cuenta,
                'header2': f'{nombre} {apellido}',
                'header3': importe_pago,
                'header4': 1,
            }
            data['data'].append(emp_dict)

        try:
            excel_data = descarga_excel(data, sheet_name='Liquidaciones')
        except Exception as e:
            error = f'Error al crear el archivo Excel de acreditaciones Galicia: {e}'
            # trace
            import traceback
            full_error = error + '\n' + traceback.format_exc()
            log.error(full_error)
            return False, error

        f = open(path, 'wb')
        f.write(excel_data)
        f.close()
        return True, None
