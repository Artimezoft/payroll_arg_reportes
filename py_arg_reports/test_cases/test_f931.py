import json

from py_arg_reports.reporters.f931.reporter import genera_txt_f931


with open('./test_cases/f931-info.json', 'r') as f:
    f931_data = json.load(f)

cuit_empresa = f931_data['cuit']
periodo = f931_data['periodo']

# Llamo a la función genera_txt_f931
resultado_descarga = genera_txt_f931(
    json_data=f931_data,
    output_path='./test_cases/downloads/',
    filename=f'{cuit_empresa}_{periodo}',
)
