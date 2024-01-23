import json

from py_arg_reports.reporters.recibo_sueldo import descargar_recibo

with open('./test_cases/liquidacion_completa.json', 'r') as f:
    liquidacion = json.load(f)

# Llamo a la función descargar_recibo
resultado_descarga = descargar_recibo(
    json_data=liquidacion,
    output_path='./downloads/',
    filename='recibo_prueba',
)
