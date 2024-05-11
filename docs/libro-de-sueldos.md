# Libro Sueldos

Para generar el PDF del libro de sueldos es necesario tener un JSON con la información de los recibos de sueldos.  

Ver modelo de JSON usado en [samples-recibo-info.json](/py_arg_reports/reporters/libro_sueldo/samples/samples-recibo-info.json)
(es el mismo modelo que el recibo de sueldos).  

El campo `tipo_concepto` usado se debe interpretar como:
  - 1: Remunerativo
  - 2: No Remunerativo
  - 3: Descuento

```python
import json

from py_arg_reports.reporters.libro_sueldo import descargar_libro

my_json = 'py_arg_reports/reporters/libro_sueldo/samples/samples-recibo-info.json
liquidacion = json.load(open(my_json, 'r'))

# Llamo a la función descargar_libro
resultado_descarga = descargar_libro(
    json_data=liquidacion,
    output_path='./downloads/',
    filename='libro-sueldo',
)
```

El archivo final estará disponible en `downloads/libro-sueldo.pdf`.  

![Libro Sueldos](/docs/images/libro-sueldo.png)