
from py_arg_reports.tools.tools import convert_to_float_if_possible


def process_reg3(cuil: str, concepto_liq: dict) -> tuple:
    """ Generacion txt de Libro Sueldos Digital
        Registro 3 Conceptos de sueldo liquidados al trabajador
        Args:
            cuil: str, CUIL del trabajador
            concepto_liq: dict, conceptos liquidados al trabajador
            Retorna:
            (Resultado, Error, Registro3)
            - True, None, str: si todo salió bien
            - False, str, None: si falla
    """
    resp = []
    key_esenciales_concepto = ['concepto', 'cantidad', 'importe']

    for concepto in concepto_liq:
        # Validaciones
        for key in key_esenciales_concepto:
            if key not in concepto:
                return False, f'Falta la clave {key} en el diccionario de conceptos', None

        cod_con = concepto['concepto'].ljust(10)
        this_cantidad = concepto['cantidad']
        this_importe = concepto['importe']
        if this_cantidad == '':
            this_cantidad = 0

        if this_importe == '':
            this_importe = 0

        try:
            this_cantidad = convert_to_float_if_possible(this_cantidad)
            this_importe = convert_to_float_if_possible(this_importe)
        except ValueError:
            return False, 'Error al convertir cantidad o importe a float', None

        temp_cant = str(round(this_cantidad * 100))[:5]
        cantidad = temp_cant.zfill(5)
        importe = round(abs(this_importe), 2) * 100
        importe = str(int(importe)).zfill(15)
        # Por default es Crédito
        if this_importe < 0:
            tipo = 'D'
        else:
            tipo = 'C'

        # Genero fila
        # Por ahora todo en unidades días
        # TODO: período ajuste retroactivo
        # https://github.com/Artimezoft/payroll_arg_reportes/issues/21
        item = f'03{cuil}{cod_con}{cantidad}D{importe}{tipo}{" " * 6}'
        resp.append(item)

    resp_final = '\r\n'.join(resp)

    return True, None, resp_final
