import logging
import os
from pathlib import Path
from numero_a_letras import numero_a_letras
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from py_arg_reports.base_reports.recibo_base_2 import my_base_recibo
from py_arg_reports.config import config_constants
from py_arg_reports.tools.num_n_date_tools import (
    float_to_format_currency,
    formatted_date_str,
    nombre_mes,
)


log = logging.getLogger(__name__)
FONT_FAMILY = config_constants['FONT_FAMILY']
FONT_FAMILY_BOLD = config_constants['FONT_FAMILY_BOLD']
FONT_SIZE_MAIN = config_constants['FONT_SIZE_MAIN']
FONT_SIZE_BODY = config_constants['FONT_SIZE_BODY']
FONT_SIZE_SMALL = config_constants['FONT_SIZE_SMALL']
EXCLUDED_CONCEPTS = [
    'CREFIS',
]


def get_recibo_info(json_data: dict) -> dict:
    """ Obtiene la información del recibo de sueldo en formato JSON
        Con datos de la empresa, empleado, liquidación, etc.
        con el formato en el ejemplo reporters/samples/samples-recibo-info.json
    """
    # Si el json está vacío, no se puede descargar
    if not json_data:
        return {
            "error": "No se puede descargar el recibo, no hay datos"
        }

    # Si faltan algunas de las keys en results, no se puede descargar
    keys_to_check = ['empresa', 'liquidacion', 'empleado', 'conceptos_liquidados', 'totales_liquidacion']
    for key in keys_to_check:
        if key not in json_data[0]:
            return {
                "error": f"No se puede descargar el recibo, no se observa {key} en los datos"
            }

    resp = {
        "empresa": {},
        "liquidaciones": [],
        "empleados": [],
        "conceptos_liquidados": [],
        'totales_liquidacion': {},
        "error": "",
    }

    serialized_emp_liqs = json_data

    # Empresa info ---------------------------------------------------------------------------
    empresa_info = serialized_emp_liqs[0]['empresa']
    resp["empresa"] = empresa_info

    # Liquidación info -----------------------------------------------------------------------
    liquidaciones_info = [emp_liq['liquidacion'] for emp_liq in serialized_emp_liqs]
    resp["liquidaciones"] = liquidaciones_info

    # Empleados info -------------------------------------------------------------------------
    empleado_list = [item['empleado'] for item in serialized_emp_liqs]
    resp["empleados"] = empleado_list

    # Conceptos info -------------------------------------------------------------------------
    conceptos_dict = {}
    totales_liquidacion_dict = {}
    for emp_liq in serialized_emp_liqs:
        legajo = emp_liq['empleado']['legajo']
        conceptos_liquidados = emp_liq['conceptos_liquidados']
        this_conceptos = []
        for concepto in conceptos_liquidados:
            code = concepto['concepto']['code']
            name = concepto['concepto']['name']
            tipo_concepto = concepto['concepto']['tipo_concepto']
            cantidad = concepto['cantidad']
            importe = concepto['importe']
            this_conceptos.append({
                'code': code,
                'name': name,
                'tipo_concepto': tipo_concepto,
                'cantidad': cantidad,
                'importe': importe,
            })

        conceptos_dict[str(legajo)] = this_conceptos
        totales_liquidacion_dict[str(legajo)] = emp_liq['totales_liquidacion']

    resp["conceptos_liquidados"] = conceptos_dict
    resp["totales_liquidacion"] = totales_liquidacion_dict

    return resp


def get_info_final_for_recibo(api_dict: dict) -> dict:
    first_liquidacion = api_dict["liquidaciones"][0]
    periodo = first_liquidacion["periodo"]["periodo"].replace('-', '/')
    company_name = api_dict["empresa"]["name"]
    cuit = api_dict["empresa"]["cuit"]
    domicilio_obj = api_dict["empresa"]["domicilio"]
    domicilio = domicilio_obj["calle"] + ' ' + domicilio_obj["numero"]
    domicilio_elements_to_add = ['piso', 'oficina', 'barrio']
    for element in domicilio_elements_to_add:
        if domicilio_obj[element]:
            domicilio += ', ' + domicilio_obj[element]

    localidad = domicilio_obj["localidad"]["name"]
    provincia = domicilio_obj["localidad"]["provincia"]["name"]
    domicilio += f', {localidad}, {provincia}'

    ultimo_pago_ss = api_dict["empresa"]["ultimo_pago_seguridad_social"]

    # Datos que varían por página, todos van a ser diccionarios con la key con el legajo, salvo el mismo legajo
    legajos = []
    fechas_pago = {}
    tipos_liquidacion = {}
    nombres_completos = {}
    cuiles = {}
    categorias = {}
    fechas_ingreso = {}
    fechas_ingreso_2 = {}
    contratos = {}
    obras_sociales = {}
    areas = {}
    posiciones = {}
    basicos = {}
    lugares_trabajo = {}
    relaciones_bancarias = {}
    conceptos_liquidados = {}
    totales_liquidacion = {}

    for ix, empleado in enumerate(api_dict["empleados"]):
        legajo = str(empleado["legajo"])
        legajos.append(legajo)

        nombre = empleado["first_name"]
        apellido = empleado["last_name"]
        nombre_completo = f'{apellido}, {nombre}'
        nombres_completos[legajo] = nombre_completo.upper()
        tipos_liquidacion[legajo] = api_dict["liquidaciones"][ix]["tipo_liquidacion"]

        cuil = empleado["cuil"]
        cuil = f'{cuil[:2]}-{cuil[2:10]}-{cuil[10:]}'
        cuiles[legajo] = cuil

        categorias[legajo] = empleado["categoria"]

        fecha_ingreso = empleado["fecha_ingreso"]
        fechas_ingreso[legajo] = formatted_date_str(fecha_ingreso)
        fecha_ingreso_2 = empleado.get("fecha_ingreso_2")
        if fecha_ingreso_2:
            fechas_ingreso_2[legajo] = formatted_date_str(fecha_ingreso_2)

        this_fecha_pago = api_dict["liquidaciones"][ix].get("fecha_pago")
        fecha_pago = formatted_date_str(this_fecha_pago) if this_fecha_pago else ''
        fechas_pago[legajo] = fecha_pago

        contratos[legajo] = empleado["contrato"]
        obras_sociales[legajo] = empleado["obra_social"]
        areas[legajo] = empleado["area"]
        posiciones[legajo] = empleado["posicion"]
        basicos[legajo] = float_to_format_currency(empleado["basico"])
        lugares_trabajo[legajo] = empleado["lugar_trabajo"]
        relaciones_bancarias[legajo] = empleado["relacion_bancaria"]

        conceptos_liquidados = api_dict["conceptos_liquidados"]
        totales_liquidacion = api_dict["totales_liquidacion"]

    resp = {
        # Período y Compañía
        "periodo": periodo,
        "company_name": company_name,
        "cuit": cuit,
        "domicilio": domicilio,

        # Empleados
        "nombres_completos": nombres_completos,
        "tipo_liquidacion": tipos_liquidacion,
        'cuiles': cuiles,
        'legajos': legajos,
        "categorias": categorias,
        "fechas_ingreso": fechas_ingreso,
        "fechas_ingreso_2": fechas_ingreso_2,
        "contratos": contratos,
        "obras_sociales": obras_sociales,
        "areas": areas,
        "posiciones": posiciones,
        "basicos": basicos,
        "lugares_trabajo": lugares_trabajo,

        # Conceptos
        "conceptos_liquidados": conceptos_liquidados,
        'totales_liquidacion': totales_liquidacion,

        # Pie de página
        "fechas_pago": fechas_pago,
        "ultimo_pago_ss": ultimo_pago_ss,
        "relaciones_bancarias": relaciones_bancarias,
    }
    return resp


class ReciboSueldo:
    """Orquesta el dibujo de un recibo individual por empleado."""

    FONT_FAMILY = config_constants['FONT_FAMILY']
    FONT_FAMILY_BOLD = config_constants['FONT_FAMILY_BOLD']

    def __init__(self, c: canvas.Canvas, coordinates: dict, info_recibo: dict, legajo: str, base_version: int = 1) -> None:
        self.c = c
        self.coordinates = coordinates
        self.info_recibo = info_recibo
        self.legajo = legajo
        self.has_duplicate = coordinates.get('has_duplicate', True)
        self.total_contribuciones = 0.0
        self.base_version = base_version

        if self.has_duplicate:
            self.font_size_main = FONT_SIZE_MAIN
            self.font_size_body = FONT_SIZE_BODY
            self.font_size_small = FONT_SIZE_SMALL
            self.base_line_between = 0.5 * cm

        else:
            self.font_size_main = FONT_SIZE_MAIN + 1
            self.font_size_body = FONT_SIZE_BODY + 1
            self.font_size_small = FONT_SIZE_SMALL + 1
            self.base_line_between = 0.7 * cm

    def _set_font(self, bold: bool = False, size: int | None = None) -> None:
        font_name = self.FONT_FAMILY_BOLD if bold else self.FONT_FAMILY
        font_size = size if size is not None else (self.font_size_main if bold else self.font_size_body)
        self.c.setFont(font_name, font_size)

    def _get_employee_data(self) -> dict:
        obra_social = self.info_recibo['obras_sociales'][self.legajo]
        if len(obra_social) > 70:
            obra_social = obra_social[:70] + '...'

        return {
            'nombre_completo': self.info_recibo['nombres_completos'][self.legajo],
            'categoria': self.info_recibo['categorias'][self.legajo],
            'posicion': self.info_recibo['posiciones'][self.legajo],
            'area': self.info_recibo['areas'][self.legajo],
            'contrato': self.info_recibo['contratos'][self.legajo],
            'obra_social': obra_social,
            'cuil': self.info_recibo['cuiles'][self.legajo],
            'fecha_ingreso': self.info_recibo['fechas_ingreso'].get(self.legajo),
            'fecha_ingreso_2': self.info_recibo['fechas_ingreso_2'].get(self.legajo),
            'fecha_pago': self.info_recibo['fechas_pago'][self.legajo],
            'basico': self.info_recibo['basicos'][self.legajo],
        }

    @staticmethod
    def draw_text_with_end_coordinate(canvas, x_end, y, text, font_family='Helvetica', font_size=8):
        # Calculate the width of the text
        text_width = canvas.stringWidth(text, font_family, font_size)

        # Adjust the starting x-coordinate to place the text's end at x_end
        x_start = x_end - text_width

        # Draw the text
        canvas.drawString(x_start, y, text)

    def textObject(self, canvas, text, max_width, x, y):
        # Create a text object with the specified max width
        text_object = canvas.beginText(0, 0)
        text_object.setTextOrigin(x, y)
        canvas_font = canvas._fontname
        canvas_font_size = canvas._fontsize
        text_object.setFont(canvas_font, canvas_font_size)

        words = text.split()
        current_line = []
        current_line_width = 0

        for word in words:
            word_width = canvas.stringWidth(word + " ", canvas_font, canvas_font_size)
            if current_line_width + word_width <= max_width:
                current_line.append(word)
                current_line_width += word_width
            else:
                text_object.textLine(" ".join(current_line))
                current_line = [word]
                current_line_width = word_width

        if current_line:
            text_object.textLine(" ".join(current_line))

        return text_object

    def draw_text_with_max_width(self, canvas, text, max_width, x, y):
        formatted_text = self.textObject(canvas, text, max_width, x, y)

        canvas.drawText(formatted_text)

    def draw_titles(self) -> None:
        coords = self.coordinates

        self._set_font(bold=True, size=self.font_size_main)
        self.c.drawString(coords['company_x'], coords['company_y'], self.info_recibo['company_name'])
        self._set_font(bold=False, size=self.font_size_main)
        self.c.drawString(coords['company_domicilio_x'], coords['company_domicilio_y'], self.info_recibo['domicilio'])
        self.c.drawString(coords['company_cuit_x'], coords['company_cuit_y'], f'CUIT: {self.info_recibo["cuit"]}')

        if self.has_duplicate:
            self._set_font(bold=True, size=self.font_size_main)
            self.c.drawString(coords['dupl_company_x'], coords['company_y'], self.info_recibo['company_name'])
            self._set_font(bold=False, size=self.font_size_main)
            self.c.drawString(coords['dupl_company_domicilio_x'], coords['company_domicilio_y'], self.info_recibo['domicilio'])
            self.c.drawString(coords['dupl_company_cuit_x'], coords['company_cuit_y'], f'CUIT: {self.info_recibo["cuit"]}')

        self.draw_liquidacion_info()
        self._set_font(bold=False, size=self.font_size_body)

        data = self._get_employee_data()
        self.c.drawString(coords['nombre_x'], coords['nombre_y'], f"Nombre: {data['nombre_completo']}")
        self.c.drawString(coords['categoria_x'], coords['categoria_y'], f"Categoria: {data['categoria']}")
        self.c.drawString(coords['posicion_x'], coords['posicion_y'], f"Posición: {data['posicion']}")
        self.c.drawString(coords['area_x'], coords['area_y'], f"Area: {data['area']}")
        self.c.drawString(coords['contrato_x'], coords['contrato_y'], f"Contrato: {data['contrato']}")
        self.c.drawString(coords['obra_social_x'], coords['obra_social_y'], f"O.Social: {data['obra_social']}", charSpace=-0.1)
        self.draw_text_with_end_coordinate(
            self.c,
            coords['legajo_e_ingreso_x_ends'],
            coords['legajo_e_ingreso_y'],
            f"Legajo: {self.legajo} - Ingreso: {data['fecha_ingreso']}"
        )
        self.draw_text_with_end_coordinate(self.c, coords['cuil_x_ends'], coords['cuil_y'], f"CUIL: {data['cuil']}")
        self.draw_text_with_end_coordinate(
            self.c,
            coords['basico_x_ends'],
            coords['basico_y'],
            f"Remuneración Asignada: {data['basico']}"
        )
        if data['fecha_ingreso_2']:
            self.draw_text_with_end_coordinate(
                self.c,
                coords['fecha_ingreso_2_x_ends'],
                coords['fecha_ingreso_2_y'],
                f"Fecha Ing. Reconocida: {data['fecha_ingreso_2']}"
            )

        if self.has_duplicate:
            self.c.drawString(coords['dupl_nombre_x'], coords['nombre_y'], f"Nombre: {data['nombre_completo']}")
            self.c.drawString(coords['dupl_categoria_x'], coords['categoria_y'], f"Categoria: {data['categoria']}")
            self.c.drawString(coords['dupl_posicion_x'], coords['posicion_y'], f"Posición: {data['posicion']}")
            self.c.drawString(coords['dupl_area_x'], coords['area_y'], f"Area: {data['area']}")
            self.c.drawString(coords['dupl_contrato_x'], coords['contrato_y'], f"Contrato: {data['contrato']}")
            self.c.drawString(coords['dupl_obra_social_x'], coords['obra_social_y'], f"O.Social: {data['obra_social']}")
            self.draw_text_with_end_coordinate(
                self.c,
                coords['dupl_legajo_e_ingreso_x_ends'],
                coords['legajo_e_ingreso_y'],
                f"Legajo: {self.legajo} - Ingreso: {data['fecha_ingreso']}"
            )
            self.draw_text_with_end_coordinate(
                self.c,
                coords['dupl_cuil_x_ends'],
                coords['cuil_y'],
                f"CUIL: {data['cuil']}"
            )
            self.draw_text_with_end_coordinate(
                self.c,
                coords['dupl_basico_x_ends'],
                coords['basico_y'],
                f"Remuneración Asignada: {data['basico']}"
            )
            if data['fecha_ingreso_2']:
                self.draw_text_with_end_coordinate(
                    self.c,
                    coords['dupl_fecha_ingreso_2_x_ends'],
                    coords['fecha_ingreso_2_y'],
                    f"Fecha Ing. Reconocida: {data['fecha_ingreso_2']}"
                )

    def draw_conceptos(self) -> None:
        coords = self.coordinates
        conceptos_liquidados = self.info_recibo['conceptos_liquidados'][self.legajo]

        this_y = coords['starting_y_conceptos']
        this_contribuciones_y = coords['starting_y_contribuciones']
        max_contribuciones_per_column = 5
        contribuciones_count = 0
        contribuciones_x = coords['conceptos_x']
        dupl_contribuciones_x = coords.get('dupl_conceptos_x')

        for concepto in conceptos_liquidados:
            code = concepto['code']
            name = concepto['name']
            tipo_concepto = concepto['tipo_concepto']
            cantidad = f"{concepto['cantidad']:.2f}" if concepto['cantidad'] != 0.0 else ''
            importe = concepto['importe']
            if code in EXCLUDED_CONCEPTS:
                continue

            if tipo_concepto in [1, 2, 3]:
                self.c.drawString(coords['conceptos_x'], this_y, name)
                self.c.drawString(coords['concepto_titles_x_cant'], this_y, str(cantidad))

                if self.has_duplicate:
                    self.c.drawString(coords['dupl_conceptos_x'], this_y, name)
                    self.c.drawString(coords['dupl_concepto_titles_x_cant'], this_y, str(cantidad))

                if tipo_concepto == 1:
                    x_to_use = coords['concepto_titles_x_rem_ends']
                    x_to_use_dupl = coords.get('dupl_concepto_titles_x_rem_ends')
                elif tipo_concepto == 2:
                    x_to_use = coords['concepto_titles_x_nr_ends']
                    x_to_use_dupl = coords.get('dupl_concepto_titles_x_nr_ends')
                else:
                    x_to_use = coords['concepto_titles_x_ap_ends']
                    x_to_use_dupl = coords.get('dupl_concepto_titles_x_ap_ends')

                self.draw_text_with_end_coordinate(
                    self.c,
                    x_to_use,
                    this_y,
                    float_to_format_currency(importe, include_currency=False)
                )
                if self.has_duplicate:
                    self.draw_text_with_end_coordinate(
                        self.c,
                        x_to_use_dupl,
                        this_y,
                        float_to_format_currency(importe, include_currency=False)
                    )
                this_y -= 0.4 * cm

            elif tipo_concepto == 4:
                if contribuciones_count >= max_contribuciones_per_column * 2 or importe == 0.0:
                    continue

                this_contribucion = name
                if cantidad:
                    this_contribucion += f" ({cantidad})"
                this_contribucion += f": {float_to_format_currency(importe, include_currency=False)}"
                self.total_contribuciones += importe

                self._set_font(bold=False, size=self.font_size_small)
                self.c.drawString(contribuciones_x, this_contribuciones_y, this_contribucion)
                if self.has_duplicate:
                    self.c.drawString(dupl_contribuciones_x, this_contribuciones_y, this_contribucion)
                contribuciones_count += 1
                self._set_font(bold=False, size=self.font_size_body)

                if contribuciones_count % max_contribuciones_per_column == 0:
                    this_contribuciones_y = coords['starting_y_contribuciones']
                    contribuciones_x += 7 * cm
                    if self.has_duplicate:
                        dupl_contribuciones_x += 7 * cm
                else:
                    this_contribuciones_y -= 0.4 * cm

    def draw_total(self) -> None:
        coords = self.coordinates
        totales = self.info_recibo['totales_liquidacion'][self.legajo]

        totales_remunerativo = totales['total_remunerativo']
        totales_no_remunerativo = totales['total_no_remunerativo']
        totales_retenciones = totales['total_retenciones']
        neto_liquidacion = totales['neto_liquidacion']
        neto_en_letras = numero_a_letras(neto_liquidacion)

        self.c.drawString(
            coords['totales_x_rem'],
            coords['starting_y_totales'],
            float_to_format_currency(totales_remunerativo, include_currency=False)
        )
        self.c.drawString(
            coords['totales_x_nr'],
            coords['starting_y_totales'],
            float_to_format_currency(totales_no_remunerativo, include_currency=False)
        )
        self.c.drawString(
            coords['totales_x_ap'],
            coords['starting_y_totales'],
            float_to_format_currency(totales_retenciones, include_currency=False)
        )
        self._set_font(bold=True, size=self.font_size_main)
        self.c.drawString(
            coords['totales_x_ap'] - 0.5 * cm,
            coords['starting_y_totales_neto'],
            float_to_format_currency(neto_liquidacion, include_currency=False)
        )
        self.c.drawString(
            coords['conceptos_x'] + 3 * cm,
            coords['contribuciones_titles_y'],
            float_to_format_currency(self.total_contribuciones, include_currency=False)
        )
        self._set_font(bold=False, size=self.font_size_body)

        if self.has_duplicate:
            self.c.drawString(
                coords['dupl_concepto_titles_x_rem'],
                coords['starting_y_totales'],
                float_to_format_currency(totales_remunerativo, include_currency=False)
            )
            self.c.drawString(
                coords['dupl_concepto_titles_x_nr'],
                coords['starting_y_totales'],
                float_to_format_currency(totales_no_remunerativo, include_currency=False)
            )
            self.c.drawString(
                coords['dupl_concepto_titles_x_ap'],
                coords['starting_y_totales'],
                float_to_format_currency(totales_retenciones, include_currency=False)
            )
            self._set_font(bold=True, size=self.font_size_main)
            self.c.drawString(
                coords['dupl_concepto_titles_x_ap'] - 0.5 * cm,
                coords['starting_y_totales_neto'], float_to_format_currency(neto_liquidacion, include_currency=False)
            )
            self.c.drawString(
                coords['dupl_conceptos_x'] + 3 * cm,
                coords['contribuciones_titles_y'],
                float_to_format_currency(self.total_contribuciones, include_currency=False)
            )

        self._set_font(bold=False, size=self.font_size_body)
        self.c.drawString(coords['company_x'], coords['neto_letras_y'], f"Son: {neto_en_letras}")
        if self.has_duplicate:
            self.c.drawString(coords['dupl_company_x'], coords['neto_letras_y'], f"Son: {neto_en_letras}")

    def draw_signature(self) -> None:
        coords = self.coordinates
        pie_de_pagina_x = coords['pie_de_pagina_x']
        pie_de_pagina_y = coords['pie_de_pagina_y']
        dupl_pie_de_pagina_x = coords.get('dupl_pie_de_pagina_x')

        pie_linea_1_y = pie_de_pagina_y
        pie_linea_2_y = pie_de_pagina_y - self.base_line_between
        pie_linea_3_y = pie_de_pagina_y - self.base_line_between * 2
        pie_linea_4_y = pie_de_pagina_y - self.base_line_between * 3

        relacion_bancaria = self.info_recibo['relaciones_bancarias'][self.legajo]
        forma_pago = relacion_bancaria['forma_pago']
        numero_cuenta = relacion_bancaria['numero_cuenta']
        cbu = relacion_bancaria['cbu']
        fecha_pago = self.info_recibo['fechas_pago'][self.legajo]

        pagado_como = "Abonado en Efectivo"
        if forma_pago.lower()[:2] == 'ch':
            pagado_como = "Abonado con Cheque"
        if numero_cuenta or cbu:
            pagado_como = f'CBU: {cbu}' if cbu else f'Cuenta: {numero_cuenta}'

        self.c.drawString(pie_de_pagina_x, pie_linea_1_y, f'{pagado_como} - Fecha: {fecha_pago}')
        self._set_font(bold=True, size=self.font_size_body)
        self.c.drawString(pie_de_pagina_x, pie_linea_2_y, "Último Depósito Aportes y Contribuciones")
        self._set_font(bold=False, size=self.font_size_body)
        if self.info_recibo['ultimo_pago_ss']['id']:
            periodo_ss = f'{nombre_mes(int(self.info_recibo["ultimo_pago_ss"]["mes"]))}'
            periodo_ss += f' {self.info_recibo["ultimo_pago_ss"]["anio"]}'
            fecha_pago_ss = formatted_date_str(self.info_recibo['ultimo_pago_ss']['fecha_pago'])
            banco_ss = self.info_recibo['ultimo_pago_ss']['banco']
            self.c.drawString(pie_de_pagina_x, pie_linea_3_y, f'Período: {periodo_ss} - {fecha_pago_ss}')
            self.c.drawString(pie_de_pagina_x, pie_linea_4_y, f'Banco: {banco_ss}')

        if self.has_duplicate:
            pie_size = 1.0 * cm
            pie_x = pie_de_pagina_x + coords['pie_de_pagina_width'] * 0.58 - 2.0 * cm
            pie_y = max(0.2 * cm, pie_linea_4_y + 0.2 * cm)
        else:
            pie_size = 1.5 * cm
            pie_x = pie_de_pagina_x + coords['pie_de_pagina_width'] * 0.42 + 0.5 * cm - 1.0 * cm + 3.0 * cm
            pie_y = max(0.2 * cm, pie_linea_4_y + 0.2 * cm) - 1.0 * cm + 1.0 * cm

        font_delta = 2 if not self.has_duplicate else 0
        self.draw_pie_chart(
            pie_x,
            pie_y,
            pie_size,
            self.info_recibo['totales_liquidacion'][self.legajo],
            self.info_recibo['conceptos_liquidados'][self.legajo],
            font_delta=font_delta,
        )

        if self.has_duplicate:
            self.c.drawString(dupl_pie_de_pagina_x, pie_linea_1_y, f'{pagado_como} - Fecha: {fecha_pago}')
            self._set_font(bold=True, size=self.font_size_body)
            self.c.drawString(dupl_pie_de_pagina_x, pie_linea_2_y, "Último Depósito Aportes y Contribuciones")
            self._set_font(bold=False, size=self.font_size_body)
            if self.info_recibo['ultimo_pago_ss']['id']:
                periodo_ss = f'{nombre_mes(int(self.info_recibo["ultimo_pago_ss"]["mes"]))}'
                periodo_ss += f' {self.info_recibo["ultimo_pago_ss"]["anio"]}'
                fecha_pago_ss = formatted_date_str(self.info_recibo['ultimo_pago_ss']['fecha_pago'])
                banco_ss = self.info_recibo['ultimo_pago_ss']['banco']
                self.c.drawString(dupl_pie_de_pagina_x, pie_linea_3_y, f'Período: {periodo_ss} - {fecha_pago_ss}')
                self.c.drawString(dupl_pie_de_pagina_x, pie_linea_4_y, f'Banco: {banco_ss}')

    def draw_empleado(self) -> None:
        """Compat layer over ReciboSueldo to preserve current public API."""
        self.draw_titles()
        self.draw_conceptos()
        self.draw_total()
        self.draw_signature()

    def draw_pie_chart(
        self,
        x: float,
        y: float,
        size: float,
        totales: dict,
        conceptos: list,
        font_delta: int = 0
    ) -> None:
        """Dibuja un gráfico de torta con la distribución salarial.
        Solo se dibuja si 'main_agrupadores' está presente en totales.
        """
        try:
            from reportlab.graphics.shapes import Drawing
            from reportlab.graphics.charts.piecharts import Pie
            from reportlab.graphics import renderPDF
            from reportlab.lib import colors as rl_colors
        except ImportError as e:
            log.error(f"[draw_pie_chart] Error importando reportlab graphics: {e}")
            return

        main_agrupadores = totales.get('main_agrupadores', {})
        if not main_agrupadores:
            log.debug("[draw_pie_chart] main_agrupadores ausente o vacío, omitiendo gráfico")
            return

        neto = totales.get('neto_liquidacion', 0)
        seg_social = main_agrupadores.get('AP_SS', 0) + main_agrupadores.get('CT_SS', 0)
        obra_social = main_agrupadores.get('AP_OS', 0) + main_agrupadores.get('CT_OS', 0)
        sindical = main_agrupadores.get('AP_SIN', 0) + main_agrupadores.get('CT_SIN', 0)

        art = next((item['importe'] for item in conceptos if item['code'] == 'CTRART'), 0)
        svida = next((item['importe'] for item in conceptos if item['code'] == 'SEGOBL'), 0)

        total_rem = totales.get('total_remunerativo', 0)
        total_no_rem = totales.get('total_no_remunerativo', 0)
        total_contribuciones = totales.get('total_contribuciones') or sum(
            item['importe'] for item in conceptos if item.get('tipo_concepto') == 4
        )
        total = totales.get('costo_conceptos') or (total_rem + total_no_rem + total_contribuciones)
        otros = max(0, total - neto - seg_social - obra_social - sindical - art - svida)

        LABELS = {
            'Neto': {
                'short': 'Neto',
                'full': 'Neto a Cobrar',
                'value': neto,
            },
            'Seg.Social': {
                'short': 'SS',
                'full': 'Seguridad Social',
                'value': seg_social,
            },
            'O.Social': {
                'short': 'OS',
                'full': 'Obra Social',
                'value': obra_social,
            },
            'Sindical': {
                'short': 'Sin',
                'full': 'Sindicato',
                'value': sindical,
            },
            'A.R.T.': {
                'short': 'ART',
                'full': 'A.R.T.',
                'value': art,
            },
            'S.Vida': {
                'short': 'SV',
                'full': 'Seguro de Vida',
                'value': svida,
            },
            'Otros': {
                'short': 'Ot',
                'full': 'Otros',
                'value': otros,
            },
        }

        slices = [
            ('Neto', neto, rl_colors.Color(0.2, 0.6, 0.2)),
            ('Seg.Social', seg_social, rl_colors.Color(0.8, 0.2, 0.2)),
            ('O.Social', obra_social, rl_colors.Color(0.2, 0.4, 0.8)),
            ('Sindical', sindical, rl_colors.Color(0.9, 0.6, 0.1)),
            ('A.R.T.', art, rl_colors.Color(0.6, 0.2, 0.6)),
            ('S.Vida', svida, rl_colors.Color(0.2, 0.8, 0.8)),
            ('Otros', otros, rl_colors.Color(0.75, 0.75, 0.75)),
        ]
        slices = [(lbl, val, col) for lbl, val, col in slices if val > 0]
        if not slices:
            log.warning("[draw_pie_chart] Todos los slices son 0, omitiendo gráfico")
            return

        try:
            # Pie (no labels — legend drawn manually below)
            d = Drawing(size, size)
            pie = Pie()
            pie.x = 0
            pie.y = 0
            pie.width = size
            pie.height = size
            pie.data = [s[1] for s in slices]
            pie.slices.strokeWidth = 0.5
            pie.slices.strokeColor = rl_colors.white
            for i, (_, _, col) in enumerate(slices):
                pie.slices[i].fillColor = col
            d.add(pie)
            pie_draw_x = x + 1 * cm
            renderPDF.draw(d, self.c, pie_draw_x, y - 0.33 * cm)

            # "Costo Total" label above the pie
            self.c.saveState()
            self.c.setFont(FONT_FAMILY_BOLD, 6 + font_delta)
            self.c.drawString(pie_draw_x, y + size + 0.1 * cm, "Total Costo")
            self.c.drawString(pie_draw_x, y + size - 0.2 * cm, float_to_format_currency(total))
            self.c.restoreState()

            # 1-column legend to the right of the pie (fixed absolute position)
            sq = 0.18 * cm
            row_h = 0.27 * cm
            legend_x = x + size + 1.8 * cm
            legend_top = y + size + 0.13 * cm

            self.c.saveState()
            self.c.setFont(FONT_FAMILY, 5 + font_delta)
            for i, (lbl, _, col) in enumerate(slices):
                short = LABELS.get(lbl, {}).get('short', lbl[:3])
                long = LABELS.get(lbl, {}).get('full', lbl)
                description = short
                if not self.has_duplicate:
                    value = LABELS.get(lbl, {}).get('value', 0)
                    description = f"{long}: {float_to_format_currency(value)}"

                lx = legend_x
                ly = legend_top - i * row_h
                self.c.setFillColor(col)
                self.c.rect(lx, ly - sq, sq, sq, fill=1, stroke=0)
                self.c.setFillColorRGB(0, 0, 0)
                self.c.drawString(lx + sq + 0.05 * cm, ly - sq + 0.02 * cm, description)
            self.c.restoreState()

            log.debug("[draw_pie_chart] Pie chart renderizado OK")
        except Exception as e:
            log.error(f"[draw_pie_chart] Error al renderizar el gráfico: {e}", exc_info=True)

    def draw_liquidacion_info(self) -> None:
        """Dibuja la información de la liquidación en el recibo."""
        text = self.info_recibo['tipo_liquidacion'][self.legajo]

        coordinates = self.coordinates
        offset_x = -0.4 * cm

        # Original - Dibuja "Liquidación Final" centrado o usa drawString para otros casos
        if text == 'Liquidación Final':
            self.c.drawString(coordinates['liquidacion_info_x'] + offset_x, coordinates['liquidacion_info_y'], text)
        else:
            self.c.drawString(coordinates['liquidacion_info_x'], coordinates['liquidacion_info_y'], text)

        # Dibuja el período en el recibo original
        self.c.drawString(coordinates['periodo_x'], coordinates['periodo_y'], self.info_recibo['periodo'])

        if coordinates.get('has_duplicate', True):
            if text == 'Liquidación Final':
                self.c.drawString(coordinates['dupl_liq_info_x'] + offset_x, coordinates['liquidacion_info_y'], text)
            else:
                self.c.drawString(coordinates['dupl_liq_info_x'], coordinates['liquidacion_info_y'], text)

            self.c.drawString(coordinates['dupl_periodo_x'], coordinates['periodo_y'], self.info_recibo['periodo'])


class ReciboDownloader:
    def __init__(self, json_data: dict, output_path: str, filename: str, base_version: int = 1):
        self.base_version = base_version
        self.json_data = json_data
        self.output_path = output_path
        self.filename = filename
        self.recibo_info = get_recibo_info(json_data)

    @staticmethod
    def get_coordinates_for_recibo(my_recibo_info: dict) -> dict:
        first_line_y = my_recibo_info['company_info_y'] + my_recibo_info['company_info_height'] - 0.35 * cm
        has_duplicate = my_recibo_info.get('has_duplicate', True)
        base_x = my_recibo_info.get('margin_x', 0) + 0.2 * cm
        base_x_ends = base_x + my_recibo_info['employee_info_width'] - 0.4 * cm
        employee_right_ends = base_x_ends if has_duplicate else (base_x_ends - 1.0 * cm)
        rem_column_shift = 0 if has_duplicate else 0.6 * cm
        nr_column_shift = 0 if has_duplicate else 0.4 * cm
        ap_column_shift = 0 if has_duplicate else 0.2 * cm
        base_line_between = 0.5 * cm
        base_line_between_2 = 0.43 * cm
        starting_y_employee_info = my_recibo_info['employee_info_y'] + my_recibo_info['employee_info_height'] - 0.45 * cm

        starting_y_conceptos = my_recibo_info['conceptos_titles_y'] - 0.45 * cm
        starting_y_contribuciones = my_recibo_info['contribuciones_titles_y'] - 0.45 * cm
        liquidacion_y_offset = -0.1 * cm if has_duplicate else -0.2 * cm
        periodo_y_offset = -0.2 * cm if has_duplicate else -0.4 * cm

        resp = {
            'has_duplicate': has_duplicate,
            'company_x': base_x,
            'company_y': first_line_y,
            'company_domicilio_x': base_x,
            'company_domicilio_y': first_line_y - base_line_between,
            'company_cuit_x': base_x,
            'company_cuit_y': first_line_y - base_line_between * 2,

            'liquidacion_info_x': my_recibo_info['liquidacion_info_x'] + my_recibo_info['liquidacion_info_width'] / 4,
            'liquidacion_info_y': first_line_y - 0.1 * cm + liquidacion_y_offset,
            'periodo_x': my_recibo_info['liquidacion_info_x'] + my_recibo_info['liquidacion_info_width'] / 4,
            'periodo_y': first_line_y - 0.8 * cm + periodo_y_offset,

            'nombre_x': base_x,
            'nombre_y': starting_y_employee_info,
            'categoria_x': base_x,
            'categoria_y': starting_y_employee_info - base_line_between_2,
            'posicion_x': base_x,
            'posicion_y': starting_y_employee_info - base_line_between_2 * 2,
            'area_x': base_x,
            'area_y': starting_y_employee_info - base_line_between_2 * 3,
            'contrato_x': base_x,
            'contrato_y': starting_y_employee_info - base_line_between_2 * 4,
            'obra_social_x': base_x,
            'obra_social_y': starting_y_employee_info - base_line_between_2 * 5,
            'legajo_e_ingreso_x_ends': employee_right_ends,
            'legajo_e_ingreso_y': starting_y_employee_info,
            'cuil_x_ends': employee_right_ends,
            'cuil_y': starting_y_employee_info - base_line_between_2,
            'basico_x_ends': employee_right_ends,
            'basico_y': starting_y_employee_info - base_line_between_2 * 2,
            'fecha_ingreso_2_x_ends': employee_right_ends,
            'fecha_ingreso_2_y': starting_y_employee_info - base_line_between_2 * 3,

            'starting_y_conceptos': starting_y_conceptos,
            'starting_y_contribuciones': starting_y_contribuciones,
            'conceptos_x': base_x,
            'concepto_titles_x_cant': my_recibo_info['concepto_titles_x_cant'],
            'concepto_titles_x_rem': my_recibo_info['concepto_titles_x_rem'],
            'concepto_titles_x_nr': my_recibo_info['concepto_titles_x_nr'],
            'concepto_titles_x_ap': my_recibo_info['concepto_titles_x_ap'],

            'concepto_titles_x_cant_ends': my_recibo_info['concepto_titles_x_rem'],
            'concepto_titles_x_rem_ends': my_recibo_info['concepto_titles_x_nr'] - rem_column_shift,
            'concepto_titles_x_nr_ends': my_recibo_info['concepto_titles_x_ap'] - nr_column_shift,
            'concepto_titles_x_ap_ends': base_x_ends - ap_column_shift,
            'starting_y_totales': my_recibo_info['starting_y_totales'],
            'starting_y_totales_neto': my_recibo_info['starting_y_totales_neto'],
            'totales_x_rem': my_recibo_info['concepto_titles_x_rem'] - rem_column_shift,
            'totales_x_nr': my_recibo_info['concepto_titles_x_nr'] - nr_column_shift,
            'totales_x_ap': my_recibo_info['concepto_titles_x_ap'] - ap_column_shift,
            'contribuciones_titles_y': my_recibo_info['contribuciones_titles_y'],
            'neto_letras_y': my_recibo_info['starting_y_totales_neto'] - base_line_between_2 + 0.05 * cm,

            'pie_de_pagina_x': base_x,
            'pie_de_pagina_y': my_recibo_info['pie_pagina_y'],
            'pie_de_pagina_width': my_recibo_info['pie_pagina_width'],
            'pie_de_pagina_height': my_recibo_info['pie_pagina_height'],
        }

        if has_duplicate:
            base_duplicate_x = my_recibo_info['duplicate_x'] + 0.2 * cm
            base_duplicate_x_ends = base_duplicate_x + my_recibo_info['employee_info_width'] - 0.4 * cm
            resp.update({
                'dupl_company_x': base_duplicate_x,
                'dupl_company_domicilio_x': base_duplicate_x,
                'dupl_company_cuit_x': base_duplicate_x,
                'dupl_liq_info_x': my_recibo_info['liquidacion_info_x_duplicate'] + my_recibo_info['liquidacion_info_width'] / 4,
                'dupl_periodo_x': my_recibo_info['liquidacion_info_x_duplicate'] + my_recibo_info['liquidacion_info_width'] / 4,
                'dupl_nombre_x': base_duplicate_x,
                'dupl_categoria_x': base_duplicate_x,
                'dupl_posicion_x': base_duplicate_x,
                'dupl_area_x': base_duplicate_x,
                'dupl_contrato_x': base_duplicate_x,
                'dupl_obra_social_x': base_duplicate_x,
                'dupl_legajo_e_ingreso_x_ends': base_duplicate_x_ends,
                'dupl_cuil_x_ends': base_duplicate_x_ends,
                'dupl_basico_x_ends': base_duplicate_x_ends,
                'dupl_fecha_ingreso_2_x_ends': base_duplicate_x_ends,
                'dupl_conceptos_x': base_duplicate_x,
                'dupl_concepto_titles_x_cant': my_recibo_info['dupl_concepto_titles_x_cant'],
                'dupl_concepto_titles_x_rem': my_recibo_info['dupl_concepto_titles_x_rem'],
                'dupl_concepto_titles_x_nr': my_recibo_info['dupl_concepto_titles_x_nr'],
                'dupl_concepto_titles_x_ap': my_recibo_info['dupl_concepto_titles_x_ap'],
                'dupl_concepto_titles_x_cant_ends': my_recibo_info['dupl_concepto_titles_x_rem'],
                'dupl_concepto_titles_x_rem_ends': my_recibo_info['dupl_concepto_titles_x_nr'],
                'dupl_concepto_titles_x_nr_ends': my_recibo_info['dupl_concepto_titles_x_ap'],
                'dupl_concepto_titles_x_ap_ends': base_duplicate_x_ends,
                'dupl_pie_de_pagina_x': base_duplicate_x,
            })

        return resp

    def draw_recibo(self, my_file_path):
        """ Dibuja el recibo de sueldo en un archivo PDF.
        """

        if self.base_version == 1:
            from py_arg_reports.base_reports.recibo_base_1 import my_base_recibo as base_fn
            pagesize = landscape(A4)
        else:
            base_fn = my_base_recibo
            pagesize = A4

        # Create a canvas
        c = canvas.Canvas(
            filename=my_file_path,
            pagesize=pagesize,
        )
        c.setTitle("Recibo de Sueldo")
        c.setAuthor("PayrollJE")

        # Get info from recibo_info
        info_recibo = get_info_final_for_recibo(self.recibo_info)

        # Add the format to the file
        my_recibo_info = base_fn(c)

        # Get coordinates for recibo
        coordinates = self.get_coordinates_for_recibo(my_recibo_info=my_recibo_info)
        legajos = info_recibo['legajos']
        for index, legajo in enumerate(legajos):
            if index > 0:
                my_recibo_info = base_fn(c)
                coordinates = self.get_coordinates_for_recibo(my_recibo_info=my_recibo_info)

            recibo_sueldo = ReciboSueldo(
                c=c,
                coordinates=coordinates,
                info_recibo=info_recibo,
                legajo=legajo,
                base_version=self.base_version
            )
            recibo_sueldo.draw_empleado()

            if index < len(legajos) - 1:
                c.showPage()

        c.save()

    def descargar_recibo(self) -> str:
        """ Descarga el recibo de sueldo en formato PDF,
            Retorna:
            - final_path, None if OK
            - False, error message if error
        """
        if self.recibo_info.get("error"):
            error_detail = self.recibo_info["error"]
            return False, error_detail

        # Cada liquidación va a tener su propia carpeta en download
        my_path = self.output_path
        if not os.path.exists(my_path):
            os.makedirs(my_path)

        if not self.filename.lower().endswith('.pdf'):
            self.filename += '.pdf'
        my_file_path = Path(my_path) / self.filename
        my_file_path = str(my_file_path)
        log.info(f"Descargando recibo en {my_file_path}")

        try:
            self.draw_recibo(my_file_path)
        except Exception as e:
            log.error(f"Error al renderizar recibo: {e}")
            return False, "Error al renderizar el recibo"

        return my_file_path, None
