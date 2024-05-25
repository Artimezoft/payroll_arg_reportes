# Acreaditacion de haberes Santander

Santander Argentina permite archivo TXT o una nueva version en excel

## Acreditacion Santander en TXT

Santander requiere un archivo TXT de campos de ancho fijo y sin separadores
Incluye un header, luego todas las filas con los registros de acreditación y un trailer
El documento con las especificaciones tècnicas està aquí
[Guía txt Santander Argentina - Pago de Haberes y Honorarios.pdf](</py_arg_reports/reporters/acreditaciones/santander/docs/Guía txt - Pago de Haberes y Honorarios.pdf>)



### Header

| Nro. | NOMBRE DE CAMPO                                      | Tipo | Long | Dec | Posicion | Descripcion | Oblig |
|------|------------------------------------------------------|------|------|-----|----------|-------------|-------|
| 1    | Tipo de Registro      | Alf  | 1    |     | 001-001  | Identificador de registro H = Header | S     |
| 2    | Número de Acuerdo (el mismo será informado por el Banco) | Num  | 17   |     | 002-018  | Número de Acuerdo que identifica a la empresa expresado en el siguiente formato: Cuit de la Empresa: 11 posiciones Nro Dig. Empresa: Fijo “0” Cod. Producto: 3 (ver: Tabla 1) Nro de Acuerdo: 2 (asignado por el Banco | S     |
| 3    | Codigo del canal      | Num  | 3    | 0   | 019-021  | Opciones: 007 Online Banking Cash Management 005 Diskette | S     |
| 4    | Numero de envìo       | Num  | 5    | 0   | 022-026  | Número secuencial de envío generado por la empresa adherida a Piryp – Pagos. (Si son varios envíos en el mismo día se tendrá que poner en el archivo 1, 00001, para el archivo 2, 00002, etc., si son en diferentes días siempre 00001). | S     |
| 5    | Reservado para usos futuros  | Num  | 5    | 0   | 027-031  | Rellenar con ceros |       |
| 6    | Reservado para usos futuros  | Alf  | 7    |     | 032-038  | Rellenar con espacios | N     |
| 7    | Validacion CUIL       | Alf  | 1    |     | 039-039  | Marca de validación de CUIL: Solo se utiliza para pagos con créditos a cuentas de Banco Río para validar que el CUIL del beneficiario informado en el envío, sea igual al CUIL del beneficiario informado en la cuenta indicada. Con “S” valida. | S     |
| 8    | Reservado para usos futuros  | Alf  | 611  |     | 046-650  | Rellenar con espacios | N     |

### Fila de cada registros

El PDF es incopiable pero 
