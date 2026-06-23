import json
import sys
from pathlib import Path

# Ensure the local workspace copy is imported, not the installed package
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from py_arg_reports.reporters.recibo_sueldo import descargar_recibo

HERE = Path(__file__).parent

with open(HERE / 'liquidacion_completa.json', 'r', encoding='utf-8') as f:
    liquidacion = json.load(f)

downloads_dir = HERE / 'downloads'
downloads_dir.mkdir(exist_ok=True)

# Base 1 – landscape, two-copy (empleado + empresa)
path, error = descargar_recibo(
    json_data=liquidacion,
    output_path=str(downloads_dir),
    filename='recibo_base1_prueba',
    base_version=1,
)
print(f'[base1] path: {path}  error: {error}')

# Base 2 – portrait, single copy
path, error = descargar_recibo(
    json_data=liquidacion,
    output_path=str(downloads_dir),
    filename='recibo_base2_prueba',
    base_version=2,
)
print(f'[base2] path: {path}  error: {error}')
