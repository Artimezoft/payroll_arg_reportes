import json

from py_arg_reports.reporters.libro_sueldo_digital.reporter import genera_txt_lsd


with open('./test_cases/lsd-info-1l.json', 'r') as f:
    lsd_data = json.load(f)

cuit_empresa = lsd_data['cuit']
periodo = lsd_data['periodo']

# Llamo a la función genera_txt_lsd con los datos del archivo lsd-info.json
resultado_descarga = genera_txt_lsd(
    json_data=lsd_data,
    output_path='./test_cases/downloads/',
    filename=f'{cuit_empresa}_{periodo}',
)

if resultado_descarga[0]:
    print('Descarga exitosa')
else:
    print('Error:', resultado_descarga[1])
