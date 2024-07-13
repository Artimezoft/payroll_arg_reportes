

def process_reg3(concepto_liq: QuerySet) -> str:
    """
    Identificación del tipo de registro	2	1	2
    CUIL del trabajador	11	3	13
    Código de concepto liquidado por el empleador	10	14	23
    Cantidad	5	24	28
    Unidades	1	29	29
    Importe	15	30	44
    Indicador Débito / Crédito	1	45	45
    Período de ajuste retroactivo	6	46	51
    """
    resp = []

    for concepto in concepto_liq:
        cuil = concepto.empleado.cuil
        cod_con = concepto.concepto.ljust(10)
        temp_cant = str(round(concepto.cantidad * 100))[:5]
        cantidad = temp_cant.zfill(5)
        importe = round(abs(concepto.importe), 2) * 100
        importe = str(int(importe)).zfill(15)
        tipo = 'D' if concepto.tipo[:2] == 'Ap' else 'C'

        if concepto.importe < 0:
            tipo = 'C' if tipo == 'D' else 'D'

        # Genero fila
        item = f'03{cuil}{cod_con}{cantidad}D{importe}{tipo}{" " * 6}'
        resp.append(item)

    resp_final = '\r\n'.join(resp)

    return resp_final
