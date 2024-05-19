from py_arg_reports.reporters.f931.tools import FORMATO_TXT_F931, sync_format

"""
Ejemplo de json

json_data

{
    "cuit": "30704552744",
    "periodo": "2024-04-01",
    "txt_empleados": [
      {
        "cuil": "23223334441",
        "nombre_completo": "GOMEZ, JUAN",
        "conyuge": 0,
        "hijos": 0,
        "condicion": "01",
        "actividad": "049",
        "obra_social": "400800",
        "adherentes": 0,
        "zona": "03",
        "modalidad_contrato": "008",
        "porc_contr_dif_ss": 0.0,
        "seguro_vida_obligatorio": true,
        "localidad": "BUENOS AIRES - 3º Cinturón",
        "porcentaje_aporte_adicional_ss": 0.0,
        "corresponde_reduccion": 0,
        "tipo_empresa": "1",
        "regimen": 1,
        "tipo_operacion": 0,
        "convencionado": 0,
        "situacion": 1,
        "situacion_1": 1,
        "dia_sr1": 1,
        "situacion_2": 0,
        "dia_sr2": 0,
        "situacion_3": 0,
        "dia_sr3": 0,
        "codigo_siniestrado": 0,
        "remuneracion_total": 797478.44,
        "remuneracion_01": 536632.24,
        "remuneracion_02": 536632.24,
        "remuneracion_03": 536632.24,
        "remuneracion_04": 797478.44,
        "remuneracion_05": 536632.24,
        "remuneracion_06": 0.0,
        "remuneracion_07": 0.0,
        "remuneracion_08": 797478.44,
        "remuneracion_09": 797478.44,
        "remuneracion_10": 529628.56,
        "remuneracion_11": 0.0,
        "no_remunerativo": 260846.2,
        "sueldo": 467314.0,
        "adicionales": 28038.84,
        "premios": 41279.4,
        "hs_extras": 0.0,
        "sac": 0.0,
        "vacaciones": 0.0,
        "zona_desfavorable": 0.0,
        "maternidad": 0.0,
        "k_dias": 30,
        "k_hs_extras": 0,
        "k_horas": 0,
        "aporte_adicional_os": 0.0,
        "importe_adicional_os": 0.0,
        "detraccion": 7003.68,
        "aporte_vol": 0.0,
        "asign_fam": 0.0,
        "capital_lrt": 0.0,
        "rectificacion": 0.0,
        "incremento": 0.0,
        "imp_exc_ap_os": 0.0,
        "imp_exc_ap_ss": 0.0
      },
      {
        "cuil": "27333333336",
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
        "convencionado": 0,
        "situacion": 1,
        "situacion_1": 1,
        "dia_sr1": 1,
        "situacion_2": 12,
        "dia_sr2": 3,
        "situacion_3": 1,
        "dia_sr3": 10,
        "codigo_siniestrado": 0,
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
    ]
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
    json_data: dict,
    output_path: str,
    filename: str = None,
) -> tuple:
    """ Genera el archivo de texto para la F931,
        Args:
            json_data: dict, datos de F931 Fijos
            output_path: str, ruta donde se guardará el archivo
            filename: str, nombre del archivo

        Retorna una tupla:
         - False, error: si falla
         - True, None: si todo salió bien
    """
    resp = None

    if not json_data.get('txt_empleados'):
        return False, 'No se puede generar el txt para el F931, no hay datos'

    # Configurar filename si usuario no lo especifica
    if not filename:
        filename = f'txt_f931_{json_data["cuit"]}_{json_data["periodo"]}'

    # Crear archivo vacio
    full_path = f'{output_path}{filename}.txt'
    with open(full_path, 'w') as f:
        f.write('')

    # Comienzo dato por dato de json_data a generar en el txt linea por linea
    for empleado in json_data['txt_empleados']:
        # Generar linea por empleado
        line = ''
        for field_name in FORMATO_TXT_F931:
            if field_name not in empleado.keys():
                return False, f'El campo {field_name} no fue encontrado en los datos'
            tipo_dato = FORMATO_TXT_F931[field_name]['type']
            if tipo_dato == 'DE':
                multiplicador = FORMATO_TXT_F931[field_name].get('multiplicador', 100)
            else:
                multiplicador = FORMATO_TXT_F931[field_name].get('multiplicador', 1)
            largo = FORMATO_TXT_F931[field_name]['long']
            info = empleado[field_name]
            info_formatted = sync_format(str(info), largo, tipo_dato, multiplicador)
            line += info_formatted
        # Agregar salto de linea
        line += '\n'
        # Escribir linea en el archivo
        with open(full_path, 'a') as f:
            f.write(line)

    return True, resp
