from pathlib import Path
from py_arg_reports.logs import get_logger
from py_arg_reports.reporters.libro_sueldo.data import translate_data
from py_arg_reports.tools.pdf import CanvasPDF, CanvaPDFBlock, Format, Rect
from py_arg_reports.tools.recibos_utils import float_to_format_currency
from reportlab.lib.units import cm


log = get_logger(__name__)
F14 = Format(font_size=14)
F10 = Format(font_size=10)
F9 = Format(font_size=8)
t10_line_sep = 0.5
t9_line_sep = 0.3


def descargar_libro(json_data: dict, output_path: str, filename: str) -> tuple:
    """ Descarga el libro sueldo en formato PDF,
        Retorna una tupla:
         - False, error: si falla
         - True, None: si todo salió bien
    """

    try:
        info_recibo = translate_data(json_data)
    except Exception as e:
        error_detail = f'Error al traducir los datos para libro sueldo: {str(e)}'
        log.error(error_detail)
        return False, error_detail

    # Cada liquidación va a tener su propia carpeta en download
    if not Path(output_path).exists():
        # create the folder
        Path(output_path).mkdir(parents=True, exist_ok=True)
    my_file_path = Path(output_path) / f'{filename}.pdf'
    log.info(f'Generando libro sueldo en {my_file_path}')

    # Mi PDF general donde voy a agregar los bloques
    PDF = CanvasPDF(
        file_path=str(my_file_path),
        title='Libro Sueldo', units=cm,
        data=info_recibo,
    )
    log.info(f'Creando PDF en {my_file_path}')

    draw_header(PDF)
    draw_footer(PDF)

    pos_y = PDF.last_y + 0.1
    empleado_h = 5
    total_rem = 0
    total_no_rem = 0
    total_desc = 0
    for empleado in info_recibo['empleados']:
        log.info(f'Generando empleado {empleado["legajo"]}')
        draw_empleado(PDF, empleado, start_y=pos_y, height=empleado_h)
        pos_y = PDF.last_y + 0.3
        total_rem += empleado['totales_liquidacion']['total_remunerativo']
        total_no_rem += empleado['totales_liquidacion']['total_no_remunerativo']
        total_desc += empleado['totales_liquidacion']['total_retenciones']

    # Agregar bloque de totales
    totales = CanvaPDFBlock(PDF, Rect(0, pos_y, 0, 3), Format(font_size=10, fill_color='#F0F0F099'))
    totales.text('Totales', bold=True, x=1, y=0.5, format_=F14)
    total_empleados = len(info_recibo['legajos'])
    totales.text(f'Cantidad de empleados: {total_empleados}', bold=True, x=12, y=0.5, format_=F10)

    total_rem2 = float_to_format_currency(total_rem)
    totales.text(f'Remunerativos {total_rem2}', bold=True, x=1, y=1.5)
    total_no_rem2 = float_to_format_currency(total_no_rem, 2)
    totales.text(f'No Remunerativos {total_no_rem2}', bold=True, x=7.3, y=1.5)
    total_desc2 = float_to_format_currency(total_desc)
    totales.text(f'Descuentos $ {total_desc2}', bold=True, x=14, y=1.5)

    neto = total_rem + total_no_rem - total_desc
    neto = float_to_format_currency(neto)
    totales.text(f'Neto a cobrar {neto}', bold=True, x=1, y=2.5, format_=F14)

    PDF.finish_page()
    PDF.save()
    return True, None


def draw_header(PDF: CanvasPDF):
    info_recibo = PDF.data
    log.info(f'Creando header en pagina {PDF.page}')
    # Agregar el bloque de headers izquiero
    header = CanvaPDFBlock(PDF, is_header=True, rect=Rect(0, 0, 0, 3.3), format_=Format(font_size=10, fill_color='#D0D0D0CC'))
    header.text('Hojas Móviles Libro Art. 52 Ley 20744', align='center', y=0.7, format_=F14)
    header.text('Folio {page}', x=17.5, y=0.7, format_=F10)
    col = [info_recibo['company_name'], info_recibo['domicilio']]
    header.text_column(col, start_x=0.1, start_y=1.3, format_=Format(font_size=10))

    # actividades
    actividades = info_recibo.get('actividades', [])

    # Verificar que haya al menos una actividad principal
    if actividades:
        apri = f'Actividad principal: {actividades[0]}'
        # Crear la lista de actividades secundarias solo si existen
        asec = [f'Actividad secundaria: {act}' for act in actividades[1:]]

        col = [apri] + asec
        header.text_column(col, start_x=0.4, start_y=2.2, line_sep=t9_line_sep, format_=F9)
    else:
        header.text(' Actividades no especificadas', x=0.4, y=2.2, format_=F9)

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
    footer.text('Hojas Móviles Libro Art. 52 Ley 20744 -pagina {page}', align='center', y=0.3)
    return footer


def draw_empleado(PDF: CanvasPDF, empleado: dict, start_y, height):
    empleado_block = CanvaPDFBlock(PDF, Rect(0, start_y, 0, height), Format(font_size=10, fill_color='#F0F0F033'))
    name = f'{empleado["legajo"]} - {empleado["nombre"]}'
    y = 0.5
    empleado_block.text(name, bold=True, x=1, y=y)
    lista = ['F. Ingreso', '', 'Remun. asignada']
    y = y + t9_line_sep + 0.1
    empleado_block.text_column(lista, start_x=1, start_y=y, line_sep=t9_line_sep, format_=F9, bold=True)
    lista = [empleado["fecha_ingreso"], empleado["fecha_ingreso_2"], empleado["basico"]]
    empleado_block.text_column(lista, start_x=4, start_y=y, line_sep=t9_line_sep, format_=F9)
    lista = ['Estado civil', 'Puesto']
    empleado_block.text_column(lista, start_x=7, start_y=y, line_sep=t9_line_sep, format_=F9, bold=True)
    lista = [empleado['estado_civil'], empleado["posicion"]]
    empleado_block.text_column(lista, start_x=10, start_y=y, line_sep=t9_line_sep, format_=F9)
    lista = ['CUIL', 'Categoría', 'Seccion']
    y = 0.5 + t9_line_sep + 0.1
    empleado_block.text_column(lista, start_x=13, start_y=y, line_sep=t9_line_sep, format_=F9, bold=True)
    lista = [empleado["cuil"], empleado["categoria"], empleado["area"]]
    empleado_block.text_column(lista, start_x=16, start_y=y, line_sep=t9_line_sep, format_=F9)

    empleado_block.line(Rect(2, 1.8, 16, 1.8), line_with=2)

    y_titles = 2.3
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
    empleado_block.text(float_to_format_currency(total_remu), x=5.5, y=y_titles, align='right', bold=True,  format_=F10)
    F7 = Format(font_size=7)
    lista = [name_cant(cpt) for cpt in remunerativos]
    empleado_block.text_column(lista, start_x=0.3, start_y=y_titles + 0.5, line_sep=t9_line_sep, format_=F7)
    lista = [float_to_format_currency(cpt['importe'], include_currency=False) for cpt in remunerativos]
    empleado_block.text_column(lista, start_x=5.5, start_y=y_titles + 0.5, align='right', line_sep=t9_line_sep, format_=F9)

    # NO REMUNERATIVOS

    # Buscar todos los conceptos no remunerativos (tipo_concepto=2)
    no_remunerativos = [c for c in conceptos if c['tipo_concepto'] == 2]
    empleado_block.text('No Remunerativos', bold=True, x=6, y=y_titles, format_=F10)
    total_no_remu = sum([cpt['importe'] for cpt in no_remunerativos])
    empleado_block.text(float_to_format_currency(total_no_remu), x=12, y=y_titles, align='right', bold=True, format_=F10)

    lista = [name_cant(cpt) for cpt in no_remunerativos]
    empleado_block.text_column(lista, start_x=6, start_y=y_titles + 0.5, line_sep=t9_line_sep, format_=F7)
    lista = [float_to_format_currency(cpt['importe'], include_currency=False) for cpt in no_remunerativos]
    empleado_block.text_column(lista, start_x=12, start_y=y_titles + 0.5, align='right', line_sep=t9_line_sep, format_=F9)

    # DESCUENTOS

    # Buscar todos los conceptos descuentos (tipo_concepto=3)
    descuentos = [c for c in conceptos if c['tipo_concepto'] == 3]
    empleado_block.text('Descuentos', bold=True, x=12.4, y=y_titles, format_=F10)
    total_desc = sum([cpt['importe'] for cpt in descuentos])
    empleado_block.text(float_to_format_currency(total_desc), x=18.7, y=y_titles, align='right', bold=True, format_=F10)

    lista = [name_cant(cpt) for cpt in descuentos]
    empleado_block.text_column(lista, start_x=12.4, start_y=y_titles + 0.5, line_sep=t9_line_sep, format_=F7)
    lista = [float_to_format_currency(cpt['importe'], include_currency=False) for cpt in descuentos]
    empleado_block.text_column(lista, start_x=18.7, start_y=y_titles + 0.5, align='right', line_sep=t9_line_sep, format_=F9)

    # NETO

    y_titles += 0.3

    empleado_block.rectangle(Rect(1, y_titles+1.6, 6, 0.6), fill_color='#D0D0D0AA')
    neto_a_cobrar = float_to_format_currency(empleado["totales_liquidacion"]["neto_liquidacion"])
    empleado_block.text(f'Neto a cobrar   {neto_a_cobrar}', bold=True, x=1.2, y=y_titles+2, format_=F10)


if __name__ == '__main__':
    """
    Esto es para hacer pruebas rapido con los archivos de ejemplo.
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
