import datetime


def process_reg1(cuit: str, periodo: datetime.date, employees: int, nro_liq: int, tipo_liq: str) -> str:
    """
    Identificacion del tipo de registro	2	1	2	Alfabético
    CUIT del empleador	11	3	13	Numérico
    Identificación del envío	2	14	15	Alfanumérico
    Período	6	16	21	Numérico
    Tipo de liquidación	1	22	22	Alfanumérico
    Número de liquidación	5	23	27	Numérico
    Dias base	2	28	29	Alfanumérico
    Cantidad de trabajadores informados en registros '04'	6	30	35	Numérico
    """

    resp = f'01{cuit}SJ'
    resp += periodo
    resp += tipo_liq
    resp += str(nro_liq).zfill(5)

    ds_base = 30
    resp += str(ds_base).zfill(2) + str(employees).zfill(6)

    return resp
