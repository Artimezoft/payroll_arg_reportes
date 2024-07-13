# Libro de Suedos Ditial

Para generar el/los txt para el Libro de Sueldos Digital es necesario tener el archivo JSON con la información necesaria.

A continuación se muestra el modelo de JSON utilizado:

* [lsd-info.json](/py_arg_reports/reporters/libro_sueldo_digital/samples/lsd-info.json)

El resultado obtenido es un/os txt correspondiente al requerido por AFIP

[Registro 1](/py_arg_reports/reporters/libro_sueldo_digital/formato_txt/registro1.csv)
[Registro 2](/py_arg_reports/reporters/libro_sueldo_digital/formato_txt/registro2.csv)
[Registro 3](/py_arg_reports/reporters/libro_sueldo_digital/formato_txt/registro3.csv)
[Registro 4](/py_arg_reports/reporters/libro_sueldo_digital/formato_txt/registro4.csv)
[Registro 5](/py_arg_reports/reporters/libro_sueldo_digital/formato_txt/registro5.csv)

```python
import json

from py_arg_reports.reporters.libro_sueldo_digital.reporter import genera_txt_lsd

my_json = 'py_arg_reports/reporters/libro_sueldo_digital/samples/lsd-info.json'
json_data = json.load(open(my_json, 'r'))

# Llamo a la función descargar_libro
resultado_descarga = genera_txt_lsd(
    json_data=json_data,
    output_path='./downloads/',
)

Argumento "filename" es opcional
```

El archivo final estará disponible en `downloads/' con el nombre asignado
Este será un txt para el caso de una liquidación o un csv para más de una.