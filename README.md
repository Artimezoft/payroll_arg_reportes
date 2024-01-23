## Reportes para Payroll en Argentina

Este repositorio tiene como objetivo generar todos los reportes necesarios para Payroll en Argentina.
recibiendo un json para cada caso y retornando los distintos reportes en los formatos según el caso pdf, txt, csv, etc.

### Reportes Legales

- F.931
- Libro de Sueldos Digital
- Libro de Sueldos
- Sicore
- F.1357


### Reportes Sindicales

- Comercio
- UOM
- UOCRA
- UTHGRA
- Etc.


### Reportes Bancarios

- Banco Galicia
- Banco Santander
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

### Uso

#### Recibo de Sueldos

**json modelo**
```
[
    {
        "empresa": {
            "pk": 1,
            "name": "Empresa de Prueba",
            "cuit": "20333333333",
            "domicilio": {
                "pk": 1,
                "calle": "Calle de Prueba",
                "numero": "123",
                "piso": null,
                "oficina": null,
                "barrio": null,
                "localidad": {
                    "pk": 1252,
                    "provincia": {
                        "pk": 10,
                        "name": "Formosa",
                        "pais": {
                            "pk": 11,
                            "code": "AR",
                            "name": "Argentina"
                        }
                    },
                    "name": "10",
                    "text": "10 (Formosa)"
                },
                "cod_postal": null
            },
            "ultimo_pago_seguridad_social": {
                "id": 31,
                "banco": "Banco De La Ciudad De Buenos Aires",
                "mes": 12,
                "anio": 2023,
                "fecha_pago": "2024-01-09",
                "empresa": 1
            }
        },
        "liquidacion": {
            "nro_liq": 0,
            "tipo_liquidacion": "Mensual",
            "periodo": {
                "periodo": "2023-12"
            },
            "fecha_pago": "2024-01-04"
        },
        "empleado": {
            "legajo": 1,
            "first_name": "Empleado 1",
            "last_name": "Apellido 1",
            "cuil": "20999999991",
            "fecha_ingreso": "2019-01-01",
            "fecha_ingreso_2": null,
            "categoria": "Vendedor B",
            "contrato": "A tiempo parcial: Indeterminado /permanente",
            "obra_social": "O.S.DE LOS EMPLEADOS DE COMERCIO Y ACTIVIDADES CIVILES",
            "area": "Area 1",
            "posicion": "Posicion 1",
            "basico": 111750.19,
            "lugar_trabajo": "25 de Mayo",
            "relacion_bancaria": {
                "forma_pago": "EFVO",
                "numero_cuenta": null,
                "cbu": null
            }
        },
        "conceptos_liquidados": [
            {
                "concepto": {
                    "code": "SUELDO",
                    "tipo_concepto": 1,
                    "name": "Sueldo Básico"
                },
                "orden": 12,
                "cantidad": 30.0,
                "importe": 111739.19
            },
            {
                "concepto": {
                    "code": "ANTIGU",
                    "tipo_concepto": 1,
                    "name": "Antiguedad"
                },
                "orden": 49,
                "cantidad": 4.0,
                "importe": 4469.5676
            }
        ],
        "totales_liquidacion": {
            "total_remunerativo": 125892.82073333333,
            "total_no_remunerativo": 28325.884664999998,
            "total_retenciones": 25357.247159624996,
            "neto_liquidacion": 128861.45823870832
        }
    },
    {
        "empresa": {
            "pk": 1,
            "name": "Empresa de Prueba",
            "cuit": "20333333333",
            "domicilio": {
                "pk": 1,
                "calle": "Calle de Prueba",
                "numero": "123",
                "piso": null,
                "oficina": null,
                "barrio": null,
                "localidad": {
                    "pk": 1252,
                    "provincia": {
                        "pk": 10,
                        "name": "Formosa",
                        "pais": {
                            "pk": 11,
                            "code": "AR",
                            "name": "Argentina"
                        }
                    },
                    "name": "10",
                    "text": "10 (Formosa)"
                },
                "cod_postal": null
            },
            "ultimo_pago_seguridad_social": {
                "id": 31,
                "banco": "Banco De La Ciudad De Buenos Aires",
                "mes": 12,
                "anio": 2023,
                "fecha_pago": "2024-01-09",
                "empresa": 1
            }
        },
        "liquidacion": {
            "nro_liq": 0,
            "tipo_liquidacion": "Mensual",
            "periodo": {
                "periodo": "2023-12"
            },
            "fecha_pago": "2024-01-04"
        },
        "empleado": {
            "legajo": 12,
            "first_name": "Juan",
            "last_name": "Gómez",
            "cuil": "20223334448",
            "fecha_ingreso": "2017-07-15",
            "fecha_ingreso_2": null,
            "categoria": "Vendedor B",
            "contrato": "A tiempo parcial: Indeterminado /permanente",
            "obra_social": "O.S.DE LOS EMPLEADOS DE COMERCIO Y ACTIVIDADES CIVILES",
            "area": "Area 1",
            "posicion": "Posicion 1",
            "basico": 111739.19,
            "lugar_trabajo": "25 de Mayo",
            "relacion_bancaria": {
                "forma_pago": "TRBA",
                "numero_cuenta": "121",
                "cbu": "1111111111111111111111"
            }
        },
        "conceptos_liquidados": [
            {
                "concepto": {
                    "code": "SUELDO",
                    "tipo_concepto": 1,
                    "name": "Sueldo Básico"
                },
                "orden": 12,
                "cantidad": 30.0,
                "importe": 111739.19
            },
            {
                "concepto": {
                    "code": "ANTIGU",
                    "tipo_concepto": 1,
                    "name": "Antiguedad"
                },
                "orden": 49,
                "cantidad": 6.0,
                "importe": 6704.3514000000005
            },
            {
                "concepto": {
                    "code": "PRESEN",
                    "tipo_concepto": 1,
                    "name": "Presentismo"
                },
                "orden": 68,
                "cantidad": 8.33,
                "importe": 9870.295116666666
            }
        ],
        "totales_liquidacion": {
            "total_remunerativo": 128313.83651666666,
            "total_no_remunerativo": 28870.613216249996,
            "total_retenciones": 25842.96345115625,
            "neto_liquidacion": 131341.48628176042
        }
    },
    {
        "empresa": {
            "pk": 1,
            "name": "Empresa de Prueba",
            "cuit": "20333333333",
            "domicilio": {
                "pk": 1,
                "calle": "Calle de Prueba",
                "numero": "123",
                "piso": null,
                "oficina": null,
                "barrio": null,
                "localidad": {
                    "pk": 1252,
                    "provincia": {
                        "pk": 10,
                        "name": "Formosa",
                        "pais": {
                            "pk": 11,
                            "code": "AR",
                            "name": "Argentina"
                        }
                    },
                    "name": "10",
                    "text": "10 (Formosa)"
                },
                "cod_postal": null
            },
            "ultimo_pago_seguridad_social": {
                "id": 31,
                "banco": "Banco De La Ciudad De Buenos Aires",
                "mes": 12,
                "anio": 2023,
                "fecha_pago": "2024-01-09",
                "empresa": 1
            }
        },
        "liquidacion": {
            "nro_liq": 0,
            "tipo_liquidacion": "Mensual",
            "periodo": {
                "periodo": "2023-12"
            },
            "fecha_pago": "2024-01-04"
        },
        "empleado": {
            "legajo": 612,
            "first_name": "Dalila Renzo",
            "last_name": "Astrada",
            "cuil": "20198517888",
            "fecha_ingreso": "1990-10-01",
            "fecha_ingreso_2": null,
            "categoria": "Administrativo B",
            "contrato": "A tiempo parcial: Indeterminado /permanente",
            "obra_social": "O.S.DE LOS EMPLEADOS DE COMERCIO Y ACTIVIDADES CIVILES",
            "area": "Area 1",
            "posicion": "Posicion 1",
            "basico": 109473.525,
            "lugar_trabajo": "25 de Mayo",
            "relacion_bancaria": {
                "forma_pago": "EFVO",
                "numero_cuenta": null,
                "cbu": null
            }
        },
        "conceptos_liquidados": [
            {
                "concepto": {
                    "code": "SUELDO",
                    "tipo_concepto": 1,
                    "name": "Sueldo Básico"
                },
                "orden": 12,
                "cantidad": 30.0,
                "importe": 109473.525
            },
            {
                "concepto": {
                    "code": "ANTIGU",
                    "tipo_concepto": 1,
                    "name": "Antiguedad"
                },
                "orden": 49,
                "cantidad": 33.0,
                "importe": 36126.263249999996
            },
            {
                "concepto": {
                    "code": "PRESEN",
                    "tipo_concepto": 1,
                    "name": "Presentismo"
                },
                "orden": 68,
                "cantidad": 8.33,
                "importe": 12133.315687499999
            },
            {
                "concepto": {
                    "code": "COMA01",
                    "tipo_concepto": 2,
                    "name": "Incremento No Remunerativo"
                },
                "orden": 60,
                "cantidad": 0.0,
                "importe": 24631.543125
            }
        ],
        "totales_liquidacion": {
            "total_remunerativo": 157733.10393749998,
            "total_no_remunerativo": 35489.9483859375,
            "total_retenciones": 31745.203977460933,
            "neto_liquidacion": 161477.84834597653
        }
    }
]
```


```python
import json

from py_arg_reports.reporters.recibo_sueldo import descargar_recibo

with open('./liquidacion_corta.json', 'r') as f:
    liquidacion = json.load(f)

# Llamo a la función descargar_recibo
resultado_descarga = descargar_recibo(
    json_data=liquidacion,
    output_path='./downloads/',
    filename='recibo_prueba',
)
```
