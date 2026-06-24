import json
import sys
from copy import deepcopy
from pathlib import Path

# Ensure the local workspace copy is imported, not the installed package
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from py_arg_reports.reporters.recibo_sueldo import descargar_recibo  # noqa: E402

HERE = Path(__file__).parent

with open(HERE / 'liquidacion_completa.json', 'r', encoding='utf-8') as f:
    liquidacion = json.load(f)


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


liquidacion_for_preview = add_mock_pie_data(liquidacion)

downloads_dir = HERE / 'downloads'
downloads_dir.mkdir(exist_ok=True)

recibo_1_name = 'recibo_1_base1_landscape'
recibo_2_name = 'recibo_2_base2_portrait'

# recibo_1 -> Base 1 (landscape, duplicated)
path, error = descargar_recibo(
    json_data=liquidacion_for_preview,
    output_path=str(downloads_dir),
    filename=recibo_1_name,
    base_version=1,
)
print(f'[recibo_1|base1] path: {path}  error: {error}')

# recibo_2 -> Base 2 (portrait, single copy)
path, error = descargar_recibo(
    json_data=liquidacion_for_preview,
    output_path=str(downloads_dir),
    filename=recibo_2_name,
    base_version=2,
)
print(f'[recibo_2|base2] path: {path}  error: {error}')
