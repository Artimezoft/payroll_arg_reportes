import json
import sys
from copy import deepcopy
from pathlib import Path

# Ensure the local workspace copy is imported, not the installed package
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from py_arg_reports.reporters.recibo_sueldo import ReciboDownloader  # noqa: E402

HERE = Path(__file__).parent

with open(HERE / 'liquidacion_completa.json', 'r', encoding='utf-8') as f:
    liquidacion = json.load(f)


CONTRIBUCIONES_SAMPLE = [
    {
        "concepto": {
            "code": "CTJUBI",
            "tipo_concepto": 4,
            "name": "Contrib.Jubilacion"
        },
        "orden": 10,
        "cantidad": 10.77,
        "importe": 73917.58
    },
    {
        "concepto": {
            "code": "CTASFA",
            "tipo_concepto": 4,
            "name": "Contrib.Asig.Familiares"
        },
        "orden": 11,
        "cantidad": 4.7,
        "importe": 32257.44
    },
    {
        "concepto": {
            "code": "CTRFNE",
            "tipo_concepto": 4,
            "name": "Contrib.Fdo.Nac.empleo"
        },
        "orden": 13,
        "cantidad": 0.94,
        "importe": 6451.49
    },
    {
        "concepto": {
            "code": "CTINSS",
            "tipo_concepto": 4,
            "name": "Contrib.INSSJP"
        },
        "orden": 15,
        "cantidad": 1.59,
        "importe": 10912.62
    },
    {
        "concepto": {
            "code": "CTOBSO",
            "tipo_concepto": 4,
            "name": "Contrib.Obra Social"
        },
        "orden": 17,
        "cantidad": 5.1,
        "importe": 77456.79
    },
    {
        "concepto": {
            "code": "CTANSS",
            "tipo_concepto": 4,
            "name": "Contrib.Fdo Solidario Red."
        },
        "orden": 19,
        "cantidad": 0.9,
        "importe": 13668.85
    },
    {
        "concepto": {
            "code": "CTRART",
            "tipo_concepto": 4,
            "name": "Contrib.A.R.T."
        },
        "orden": 21,
        "cantidad": 3.75,
        "importe": 30241.76
    },
    {
        "concepto": {
            "code": "SEGOBL",
            "tipo_concepto": 4,
            "name": "Seguro de Vida Obligatorio"
        },
        "orden": 50,
        "cantidad": 0.0,
        "importe": 424.62
    },
    {
        "concepto": {
            "code": "INACAP",
            "tipo_concepto": 4,
            "name": "Contribucion INACAP"
        },
        "orden": 50,
        "cantidad": 0.0,
        "importe": 5481.24
    },
    {
        "concepto": {
            "code": "CTOSEX",
            "tipo_concepto": 4,
            "name": "Contribucion Extraordinaria OSECAC"
        },
        "orden": 80,
        "cantidad": 0.0,
        "importe": 28000.0
    },
]


def apply_contribuciones_to_all_employees(data: list) -> list:
    """Injects the same tipo 4 contribuciones list into every employee payload."""
    updated = deepcopy(data)
    for item in updated:
        conceptos = item.get('conceptos_liquidados', [])
        conceptos_no_tipo4 = [c for c in conceptos if c.get('concepto', {}).get('tipo_concepto') != 4]
        item['conceptos_liquidados'] = conceptos_no_tipo4 + deepcopy(CONTRIBUCIONES_SAMPLE)
    return updated


def add_mock_pie_data(data: list) -> list:
    """Adds chart-friendly mock totals so the pie chart always renders in previews."""
    with_chart_data = deepcopy(data)
    for item in with_chart_data:
        totales = item.get('totales_liquidacion', {})
        if not totales.get('main_agrupadores'):
            totales['main_agrupadores'] = {
                'AP_SS': 12000,
                'CT_SS': 18000,
                'AP_OS': 7000,
                'CT_OS': 9000,
                'AP_SIN': 1500,
                'CT_SIN': 2500,
            }

        if not totales.get('costo_conceptos'):
            conceptos = item.get('conceptos_liquidados', [])
            totales['costo_conceptos'] = round(sum(c.get('importe', 0) for c in conceptos), 2)

        item['totales_liquidacion'] = totales

    return with_chart_data


liquidacion_with_contribuciones = apply_contribuciones_to_all_employees(liquidacion)
liquidacion_for_preview = add_mock_pie_data(liquidacion_with_contribuciones)

downloads_dir = HERE / 'downloads'
downloads_dir.mkdir(exist_ok=True)

recibo_1_name = 'recibo_1_base1_landscape'
recibo_2_name = 'recibo_2_base2_portrait'

# recibo_1 -> Base 1 (landscape, duplicated)
recibo_dwn_1 = ReciboDownloader(
    json_data=liquidacion_for_preview,
    output_path=str(downloads_dir),
    filename=recibo_1_name,
    base_version=1,
)
path, error = recibo_dwn_1.descargar_recibo()


print(f'[recibo_1|base1] path: {path}  error: {error}')

# recibo_2 -> Base 2 (portrait, single copy)
recibo_dwn_2 = ReciboDownloader(
    json_data=liquidacion_for_preview,
    output_path=str(downloads_dir),
    filename=recibo_2_name,
    base_version=2,
)
path, error = recibo_dwn_2.descargar_recibo()
print(f'[recibo_2|base2] path: {path}  error: {error}')
