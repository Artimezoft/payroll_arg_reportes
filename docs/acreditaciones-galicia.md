# Acreaditacion de haberes Galicia

Galicia usa un archivo Excel para acreditar haberes de empleados que tienen cuenta en Galicia.  
Para _Sistema Nacional de Pagos_ (SNP) usa un archivo TXT.  

## Acreditacion Galicia en Excel

El documento [Pago de sueldos.pdf](</py_arg_reports/reporters/acreditaciones/galicia/docs/Sueldosporarchivo.pdf>)
describe como se debe armar el archivo Excel para acreditar haberes en Galicia.  

El archivode Excel debe tener una planilla con las columnas:
 - Cuenta: Nro de cuenta en Galicia
 - Nombre: Nombre del empleado
 - Importe: Importe a acreditar
 - Concepto: Siempre en 1 (Sueldo)

## Acreditaciones Galicia en TXT

Galicia usa un archivo TXT para acreditar haberes de empleados que NO tienen cuenta en Galicia.  
SNP (Sistema Nacional de Pagos) usa un archivo TXT con header, footer y lineas de 150 carcateres fijos.  
La documentacion de como construir estos archivos de texto no esta publicada. Si la conoces, por favor compartila.

## Datos de entrada

Se requiere que transformes tus datos de origen a un JSON con la estructura definida en
[este archivo](/py_arg_reports/reporters/acreditaciones/data/sample-galicia.json)

Ejemplo:

```json
{
    "empleados": [
        {
            "nombre": "Juan", "apellido": "Perez",
            "importe_pago": "1236119.04",
            "nro_cuenta": "00209023941002"
        },{
            "nombre": "Pedro", "apellido": "Argento",
            "importe_pago": "5216108.17",
            "nro_cuenta": "00209023941003"
        },
        ...
    ]
}
```

## Ejemplo de uso

```python

import json
from py_arg_reports.reporters.acreditaciones.galicia import AcreditacionGalicia

data = json.load(open('sample.json'))
acreditacion = AcreditacionGalicia(data)
destination = 'galicia.xls'
process, error = acreditacion.generate_file(destination)
if not process:
    print(error)
else:
    print('OK')
```

### Resultado

Se espera un archivo de Excel de esta forma

![Resultado Excel](/py_arg_reports/reporters/acreditaciones/galicia/docs/acreditacion-galicia-xlsx.png)

### Tests

Esta funcionalidad esta probada en `payroll_arg_reportes/tests/acreditaciones/galicia` de manera bastante completa.  
