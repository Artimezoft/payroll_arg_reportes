
"""
Ejemplo de archivos

json_f931f

{
    "cuil": "27333333333",
    "nombre_completo": "GODOY, LAURA",
    "conyuge": 0,
    "hijos": 0,
    "condicion": "01",
    "actividad": "049",
    "obra_social": "126205",
    "adherentes": 0,
    "zona": "18",
    "modalidad_contrato": "001",
    "porc_contr_dif_ss": 0.0,
    "seguro_vida_obligatorio": true,
    "localidad": "CORDOBA - Gran Córdoba",
    "porcentaje_aporte_adicional_ss": 0.0,
    "corresponde_reduccion": 0,
    "tipo_empresa": "1",
    "regimen": 1,
    "tipo_operacion": 0,
    "convencionado": 0
}

f931v

{
    "cuil": "27333333333",
    "situacion": 1,
    "situacion_1": 1,
    "dia_sr1": 1,
    "situacion_2": 12,
    "dia_sr2": 3,
    "situacion_3": 1,
    "dia_sr3": 10,
    "codigo_siniestrado": 0
}

f931i

{
    "cuil": "27333333333",
    "remuneracion_total": 425760.49,
    "remuneracion_01": 278191.37,
    "remuneracion_02": 278191.37,
    "remuneracion_03": 278191.37,
    "remuneracion_04": 851520.98,
    "remuneracion_05": 278191.37,
    "remuneracion_06": 0.0,
    "remuneracion_07": 0.0,
    "remuneracion_08": 851520.98,
    "remuneracion_09": 425760.49,
    "remuneracion_10": 274689.53,
    "remuneracion_11": 0.0,
    "no_remunerativo": 147569.12,
    "sueldo": 178264.32,
    "adicionales": 10695.86,
    "premios": 15746.68,
    "hs_extras": 0.0,
    "sac": 0.0,
    "vacaciones": 73484.51,
    "zona_desfavorable": 0.0,
    "maternidad": 0.0,
    "k_dias": 31,
    "k_hs_extras": 0,
    "k_horas": 0,
    "aporte_adicional_os": 0.0,
    "importe_adicional_os": 0.0,
    "detraccion": 3501.84,
    "aporte_vol": 0.0,
    "asign_fam": 0.0,
    "capital_lrt": 0.0,
    "rectificacion": 0.0,
    "incremento": 0.0,
    "imp_exc_ap_os": 0.0,
    "imp_exc_ap_ss": 0.0
}

Formato txt

Descripcion del campo	Desde	Longitud
CUIL	1	11
Apellido y Nombre	12	30
Cónyuge	42	1
Cantidad de Hijos	43	2
Codigo de Situación	45	2
Codigo de Condición	47	2
Código de Actividad	49	3
Código de Zona	52	2
Porcentaje de Aporte Adicional SS	54	5
Código de Modalidad de Contratación	59	3
Código de Obra Social	62	6
Cantidad de Adherentes	68	2
Remuneración Total	70	12
Remuneración Imponible 1	82	12
Asignaciones Familiares Pagadas	94	9
Importe Aporte Voluntario	103	9
Importe Adicional OS	112	9
Importe Excedentes Aportes SS	121	9
Importe Excedentes Aportes OS	130	9
Provincia Localidad	139	50
Remuneración Imponible 2	189	12
Remuneración Imponible 3	201	12
Remuneración Imponible 4	213	12
Código de Siniestrado	225	2
Marca de Corresponde Reducción	227	1
Capital de Recomposición de LRT	228	9
Tipo de empresa	237	1
Aporte Adicional de Obra Social	238	9
Regimen	247	1
Situación de Revista 1	248	2
Dia inicio Situación de Revista 1	250	2
Situación de Revista 2	252	2
Dia inicio Situación de Revista 2	254	2
Situación de Revista 3	256	2
Dia inicio Situación de Revista 3	258	2
Sueldo + Adicionales	260	12
SAC	272	12
Horas Extra	284	12
Zona desfavorable	296	12
Vacaciones	308	12
Cantidad de días trabajados	320	9
Remuneración Imponible 5	329	12
Trabajador Convencionado 0-No 1-Si	341	1
Remuneración Imponible 6	342	12
Tipo de Operación	354	1
Adicionales	355	12
Premios	367	12
Rem.Dec.788/05 - Rem Impon. 8	379	12
Remuneración Imponible 7	391	12
Cantidad de Horas Extras	403	3
Conceptos no remunerativos	406	12
Maternidad	418	12
Rectificación de remuneración	430	9
Remuneración Imponible 9	439	12
Contribucion tarea diferencial (%)	451	9
Horas trabajadas	460	3
Seguro Colectivo de Vida Obligatorio	463	1
Importe a detraer Ley 27430	464	12
Incremento Salarial	476	12
Remuneración Imponible 11	488	12
"""


def genera_txt_f931(
    json_f931f: dict,
    json_f931v: dict,
    json_f931i: dict,
    output_path: str,
    filename: str
) -> tuple:
    """ Genera el archivo de texto para la F931,
        Args:
            json_f931f: dict, datos de F931 Fijos
            json_f931v: dict, datos de F931 Variables
            json_f931i: dict, datos de F931 Importes
            output_path: str, ruta donde se guardará el archivo
            filename: str, nombre del archivo

        Retorna una tupla:
         - False, error: si falla
         - True, None: si todo salió bien
    """
    resp = None

    return True, resp