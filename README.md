## Reportes para Payroll en Argentina

Este repositorio tiene como objetivo generar todos los reportes necesarios para Payroll en Argentina.
recibiendo un json para cada caso y retornando los distintos reportes en los formatos según el caso pdf, txt, csv, etc.

Para generar cada reporte esperamos que tengas tus datos estructurados en los formatos esperados en esta librería. Es posible
que necesites adaptarlos. Una vez estructurados en el formato esperado por cada reporte, todo lo demás estará resuelto.  

Notas generales:
 - El campo `tipo_concepto` usado se debe interpretar como:
   - 1: Remunerativo
   - 2: No Remunerativo
   - 3: Descuento
 - Los campos `pk` se refieren a _primary key_ y no son necesarios para la generación de los reportes.
 - Puede haber más campos en tus datos, esta librería solo necesita los campos que se mencionan en cada reporte.

### Reportes Legales

- [Recibo de Sueldos](https://github.com/Artimezoft/payroll_arg_reportes/blob/develop/docs/recibo-de-sueldos.md)
- [F.931](https://github.com/Artimezoft/payroll_arg_reportes/blob/develop/docs/f931.md)
- [Libro de Sueldos Digital](https://github.com/Artimezoft/payroll_arg_reportes/blob/develop/docs/libro-de-sueldos-digital.md)
- [Libro de Sueldos](https://github.com/Artimezoft/payroll_arg_reportes/blob/develop/docs/libro-de-sueldos.md)
- Sicore
- F.1357


### Reportes Sindicales

- Comercio
- UOM
- UOCRA
- UTHGRA
- Etc.


### Reportes Bancarios

- [Banco Galicia](https://github.com/Artimezoft/payroll_arg_reportes/blob/develop/docs/acreditaciones-galicia.md)
- [Banco Santander](https://github.com/Artimezoft/payroll_arg_reportes/blob/develop/docs/acreditaciones-santander.md)
- Banco Nación
- Etc.


### Reportes de Liquidación

- Resumen de Liquidación
- Conceptos Liquidados por Empleado
- Planilla de Ganancias

### Reportes Informativos

- Lista de empleados
- Lista de empleados con datos personales
- Etc.


## Instalación

```bash
pip install payroll-arg-reportes
```
## Muestra

### Libro sueldos

![Libro Sueldos](https://raw.githubusercontent.com/Artimezoft/payroll_arg_reportes/develop/docs/images/libro-sueldo.png)

### Acreditaciones Galicia

![Resultado Excel](https://raw.githubusercontent.com/Artimezoft/payroll_arg_reportes/develop/py_arg_reports/reporters/acreditaciones/galicia/docs/acreditacion-galicia-xlsx.png)

### Acreditaciones Santander

```
H301234567800011000070000100000       S                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
D 0          71626RC2025010000000000000Juan Perez                    Domicilio completo, Mendiolaza, Córdoba, Arg       00000    00000000000000000000000000000000000000000000000000000000000000000000000000000000000           20345678901                                                                                                                                                                  N005404720001000000012345678901000000002025020100000012361190050   00000000000   00000000000   00000000000   0000000000000000000000000 00000000000000000                                                                                                      
D 0          60420RC2025010000000000000Victoria Velez                San Fe 511, Unquillo, Córdoba, Arg                 00000    00000000000000000000000000000000000000000000000000000000000000000000000000000000000           20244478711                                                                                                                                                                  N005402854001000000012345678902000000002025020100000009361073250   00000000000   00000000000   00000000000   0000000000000000000000000 00000000000000000                                                                                                      
T0000000000000000000002172226330000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
```
