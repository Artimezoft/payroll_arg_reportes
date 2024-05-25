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

acreditacion = AcreditacionSantander()
