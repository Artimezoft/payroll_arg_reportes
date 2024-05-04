import os
from py_arg_reports.logs import get_logger
from py_arg_reports.reporters.libro_sueldo.info import get_recibo_info, get_info_final_for_libro_sueldo
from py_arg_reports.tools.base import CanvasPDF, CanvaPDFBlock, Format, Rect
from reportlab.lib.units import cm


log = get_logger(__name__)
F14 = Format(font_size=14)
F10 = Format(font_size=10)
F9 = Format(font_size=9)
t10_line_sep = 0.5
t9_line_sep = 0.35


def descargar_libro(json_data: dict, output_path: str, filename: str) -> str:
    """ Descarga el libro sueldo en formato PDF,
        Retorna error si lo hay
    """

    recibo_info = get_recibo_info(json_data)
    if recibo_info.get("error"):
        error_detail = recibo_info["error"]
        log.error(f'Error al obtener la info del recibo: {error_detail}')
        return error_detail

    # Get info from recibo_info
    info_recibo = get_info_final_for_libro_sueldo(recibo_info)
    test_info_tecibo = 'py_arg_reports/reporters/libro_sueldo/samples/imfo-recibo.json'
    info_recibo = json.load(open(test_info_tecibo))

    # Cada liquidación va a tener su propia carpeta en download
    my_path = output_path
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    my_file_path = f'{my_path}{filename}.pdf'
    log.info(f'Generando libro sueldo en {my_file_path}')

    # Mi PDF general donde voy a agregar los bloques
    PDF = CanvasPDF(
        file_path=my_file_path,
        title='Libro Sueldo', units=cm,
        data=info_recibo,
    )
    log.info(f'Creando PDF en {my_file_path}')

    draw_header(PDF)
    draw_footer(PDF)

    pos_y = PDF.last_y + 0.1
    empleado_h = 5.5
    for legajo in info_recibo['legajos']:
        log.info(f'Generando empleado {legajo}')
        empleado = {
            'nombre': info_recibo['nombres_completos'].get(legajo),
            'cuil': info_recibo['cuiles'].get(legajo),
            'legajo': legajo,
            'categoria': info_recibo['categorias'].get(legajo),
            'fecha_ingreso': info_recibo['fechas_ingreso'].get(legajo),
            'fecha_ingreso_2': info_recibo['fechas_ingreso_2'].get(legajo),
            'contrato': info_recibo['contratos'].get(legajo),
            'obra_social': info_recibo['obras_sociales'].get(legajo),
            'area': info_recibo['areas'].get(legajo),
            'posicion': info_recibo['posiciones'].get(legajo),
            'basico': info_recibo['basicos'].get(legajo),
            'lugar_trabajo': info_recibo['lugares_trabajo'].get(legajo),
            'conceptos_liquidados': info_recibo['conceptos_liquidados'].get(legajo),
            'totales_liquidacion': info_recibo['totales_liquidacion'].get(legajo),
            'relacion_bancaria': info_recibo['relaciones_bancarias'].get(legajo),
        }
        draw_empleado(PDF, empleado, start_y=pos_y, height=empleado_h)
        pos_y = PDF.last_y + 0.3

    PDF.finish_page()
    PDF.save()


def draw_header(PDF: CanvasPDF):
    info_recibo = PDF.data
    log.info(f'Creando header en pagina {PDF.page}')
    # Agregar el bloque de headers izquiero
    header = CanvaPDFBlock(PDF, is_header=True, rect=Rect(0, 0, 0, 3.3), format_=Format(font_size=10, fill_color='#D0D0D0CC'))
    header.text('Hojas Móviles Libro Art. 52 Ley 20744', align='center', y=0.7, format_=F14)
    header.text(f'Folio {PDF.page}', x=17.5, y=0.7, format_=F10)
    col = [info_recibo['company_name'], info_recibo['domicilio']]
    header.text_column(col, start_x=0.1, start_y=1.3, format_=Format(font_size=10))
    # actividades
    actividades = ['No tenemos actividades 7777', 'Esta deberia ser la secundaria 1', 'Esta deberia ser la secundaria 2']
    apri = f'Actividad principal: {actividades[0]}'
    asec = [f'Actividad secundaria: {act}' for act in actividades[1:]]
    col = [apri] + asec
    header.text_column(col, start_x=0.4, start_y=2.2, line_sep=t9_line_sep, format_=F9)

    # Agregar el bloque de headers derecho
    per = f'Periodo {info_recibo["tipo_liquidacion"]} {info_recibo["periodo"]}'
    col = ["CUIT: " + info_recibo['cuit'], per]
    header.text_column(col, start_x=13, start_y=1.3, format_=F10)
    return header


def draw_footer(PDF: CanvasPDF):
    log.info(f'Creando footer en pagina {PDF.page}')
    footer = CanvaPDFBlock(
        PDF, is_footer=True,
        rect=Rect(0, PDF.height-1, 0, 0.5), format_=Format(font_size=8, fill_color='#D0D0D0')
    )
    footer.text(f'Hojas Móviles Libro Art. 52 Ley 20744 -pagina {PDF.page}', align='center', y=0.3)
    return footer


def draw_empleado(PDF: CanvasPDF, empleado: dict, start_y, height):
    empleado_block = CanvaPDFBlock(PDF, Rect(0, start_y, 0, height), Format(font_size=10, fill_color='#F0F0F099'))
    name = f'{empleado["legajo"]} - {empleado["nombre"]}'
    y = 0.5
    empleado_block.text(name, bold=True, x=1, y=y)
    lista = ['F. Ingreso', 'F. Egreso', 'Remun. asignada']
    y = y + t9_line_sep + 0.1
    empleado_block.text_column(lista, start_x=1, start_y=y, line_sep=t9_line_sep, format_=F9, bold=True)
    lista = [empleado["fecha_ingreso"], empleado["fecha_ingreso_2"], empleado["basico"]]
    empleado_block.text_column(lista, start_x=4, start_y=y, line_sep=t9_line_sep, format_=F9)
    lista = ['Estado civil', 'Puesto']
    empleado_block.text_column(lista, start_x=7, start_y=y, line_sep=t9_line_sep, format_=F9, bold=True)
    lista = ['FALTA', empleado["posicion"]]
    empleado_block.text_column(lista, start_x=10, start_y=y, line_sep=t9_line_sep, format_=F9)
    lista = ['CUIL', 'Categoría', 'Seccion']
    y = 0.5 + t9_line_sep + 0.1
    empleado_block.text_column(lista, start_x=13, start_y=y, line_sep=t9_line_sep, format_=F9, bold=True)
    lista = [empleado["cuil"], empleado["categoria"], empleado["area"]]
    empleado_block.text_column(lista, start_x=16, start_y=y, line_sep=t9_line_sep, format_=F9)

    empleado_block.line(Rect(2, 2, 16, 2), line_with=2)

    y_titles = 2.5
    # Los tipos de conceptos son:
    # 1 Remunerativos
    # 2 No Remunerativos
    # 3 Descuentos
    conceptos = empleado["conceptos_liquidados"]

    def name_cant(cpt):
        """ No bre y (cantidad) """
        cantidad = cpt.get('cantidad')
        final = cpt['name']
        if cantidad:
            final = f'{final} ({cantidad})'
        return final

    # REMUNERATIVOS

    # Buscar todos los conceptos remunerativos (tipo_concepto=1)
    remunerativos = [c for c in conceptos if c['tipo_concepto'] == 1]
    empleado_block.text('Remunerativos', bold=True, x=0.3, y=y_titles, format_=F10)
    total_remu = sum([cpt['importe'] for cpt in remunerativos])
    empleado_block.text(str(round(total_remu, 2)), x=5.5, y=y_titles, align='right', bold=True,  format_=F10)

    lista = [name_cant(cpt) for cpt in remunerativos]
    empleado_block.text_column(lista, start_x=0.3, start_y=y_titles + 0.5, line_sep=t9_line_sep, format_=F9)
    lista = [str(round(cpt['importe'], 2)) for cpt in remunerativos]
    empleado_block.text_column(lista, start_x=5.5, start_y=y_titles + 0.5, align='right', line_sep=t9_line_sep, format_=F9)

    # NO REMUNERATIVOS

    # Buscar todos los conceptos no remunerativos (tipo_concepto=2)
    no_remunerativos = [c for c in conceptos if c['tipo_concepto'] == 2]
    empleado_block.text('No Remunerativos', bold=True, x=6, y=y_titles, format_=F10)
    total_no_remu = sum([cpt['importe'] for cpt in no_remunerativos])
    empleado_block.text(str(round(total_no_remu, 2)), x=12, y=y_titles, align='right', bold=True, format_=F10)

    lista = [name_cant(cpt) for cpt in no_remunerativos]
    empleado_block.text_column(lista, start_x=6, start_y=y_titles + 0.5, line_sep=t9_line_sep, format_=F9)
    lista = [str(round(cpt['importe'], 2)) for cpt in no_remunerativos]
    empleado_block.text_column(lista, start_x=12, start_y=y_titles + 0.5, align='right', line_sep=t9_line_sep, format_=F9)

    # DESCUENTOS

    # Buscar todos los conceptos descuentos (tipo_concepto=3)
    descuentos = [c for c in conceptos if c['tipo_concepto'] == 3]
    empleado_block.text('Descuentos', bold=True, x=12.4, y=y_titles, format_=F10)
    total_desc = sum([cpt['importe'] for cpt in descuentos])
    empleado_block.text(str(round(total_desc, 2)), x=18.7, y=y_titles, align='right', bold=True, format_=F10)

    lista = [name_cant(cpt) for cpt in descuentos]
    empleado_block.text_column(lista, start_x=12.4, start_y=y_titles + 0.5, line_sep=t9_line_sep, format_=F9)
    lista = [str(round(cpt['importe'], 2)) for cpt in descuentos]
    empleado_block.text_column(lista, start_x=18.7, start_y=y_titles + 0.5, align='right', line_sep=t9_line_sep, format_=F9)

    empleado_block.rectangle(Rect(1, y_titles+2, 6, 0.6), fill_color='#D0D0D0AA')
    neto_a_cobrar = round(empleado["totales_liquidacion"]["neto_liquidacion"], 2)
    empleado_block.text(f'Neto a cobrar $ {neto_a_cobrar}', bold=True, x=1.2, y=y_titles+2.4, format_=F10)


if __name__ == '__main__':
    """
    Esto es para hacer pruebas rapido con los arhcivos de ejemplo.
    Dejar para hacer correcciones rápidas.
    En estas pruebas escupir los logs en la consola
    """
    import json
    # Descargar el libro
    json_data_test_file = 'py_arg_reports/reporters/libro_sueldo/samples/samples-recibo-info.json'
    json_data = json.load(open(json_data_test_file))
    output_path = 'download/'
    filename = 'libro-sueldo'
    descargar_libro(json_data, output_path, filename)
