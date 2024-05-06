import json
from py_arg_reports.reporters.libro_sueldo import descargar_libro


with open('./test_cases/liquidacion_completa.json', 'r') as f:
    liquidacion = json.load(f)

# Llamo a la función descargar_recibo
libro = descargar_libro(
    json_data=liquidacion,
    output_path='./downloads/',
    filename='libro_prueba',
)
