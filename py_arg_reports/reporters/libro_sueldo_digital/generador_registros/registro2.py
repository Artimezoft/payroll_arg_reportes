import datetime

from django.db.models.query import QuerySet


def process_reg2(leg_liqs: QuerySet, payday: datetime.date, forma_pago: str) -> str:
    """
    Identificacion del tipo de registro	2	1	2
    CUIL del trabajador	11	3	13
    Legajo del trabajador	10	14	23
    Dependencia de revista del trabajador	50	24	73
    CBU de acreditación del pago	22	74	95
    Cantidad de días para proporcionar tope	3	96	98
    Fecha de pago	8	99	106
    Fecha de rúbrica	8	107	114
    Forma de pago	1	115	115
    """
    resp = []
    for id_legajo in leg_liqs:
        empleado = Empleado.objects.get(id=id_legajo['empleado'])
        cuil = empleado.cuil
        leg = str(empleado.leg).zfill(10)

        area = " " * 50 if not empleado.area else empleado.area.ljust(50)
        fecha_pago = payday.strftime('%Y%m%d')
        # Si acredita informo el CBU, el CBU está o no está, pero no puede ser más corto
        if forma_pago == '3' and empleado.cbu:
            cbu = empleado.cbu
        else:
            cbu = " " * 22
        fecha_rubrica = " " * 8

        item = f'02{cuil}{leg}{area}{cbu}030{fecha_pago}{fecha_rubrica}{forma_pago}'

        resp.append(item)

    resp_final = '\r\n'.join(resp)

    return resp_final
