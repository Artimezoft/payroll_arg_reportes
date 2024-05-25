# Acreaditacion de haberes Santander

Santander Argentina permite archivo TXT o una nueva version en excel

## Acreditacion Santander en TXT

Santander requiere un archivo TXT de campos de ancho fijo y sin separadores
Incluye un header, luego todas las filas con los registros de acreditación y un trailer
El documento con las especificaciones tècnicas està aquí
[Guía txt Santander Argentina - Pago de Haberes y Honorarios.pdf](</py_arg_reports/reporters/acreditaciones/santander/docs/Guía txt - Pago de Haberes y Honorarios.pdf>)


## Datos de entrada

Se requiere que transformes tus datos de origen a un JSON con la estructura definida en
[este archivo](/py_arg_reports/reporters/acreditaciones/data/sample.json)

## Ejemplo de uso

```python

import json
from py_arg_reports.reporters.acreditaciones.santander import AcreditacionSantander

data = json.load(open('sample.json'))
acreditacion = AcreditacionSantander(data)
destination = 'santa.txt'
process, error = acreditacion.generate_file(destination)
if not process:
    print(error)
else:
    print('OK')
    # show results file
    f = open(destination)
    text = f.read()
    f.close()
    print(text)
```

Resultado

```
H301234567800011000070000100000       S                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
D 0          71626RC         2025010000Juan Perez                    Domicilio completo, Mendiolaza, Córdoba, Arg       00000    00000000000000000000000000000000000000000000000000000000000000000000000000000000000           20345678901                                                                                                                                                                  N005499999999999999999999999999000000002025020100000012361190050   00000000000   00000000000   00000000000   0000000000000000000000000 00000000000000000                                                                                                      
D 0          60420RC         2025010000Victoria Velez                San Fe 511, Unquillo, Córdoba, Arg                 00000    00000000000000000000000000000000000000000000000000000000000000000000000000000000000           20244478711                                                                                                                                                                  N005499999999999999999999999999000000002025020100000009361073250   00000000000   00000000000   00000000000   0000000000000000000000000 00000000000000000                                                                                                      
T0000000000000000000002172226330000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

```
