from pathlib import Path
from py_arg_reports.logs import get_logger
from py_arg_reports.reporters.libro_sueldo.data import translate_data
from py_arg_reports.tools.pdf import CanvasPDF, CanvaPDFBlock, Format, Rect
from py_arg_reports.tools.recibos_utils import float_to_format_currency
from reportlab.lib.units import cm


log = get_logger(__name__)
F10 = Format(font_size=10)
F7 = Format(font_size=7)

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
    totales = CanvaPDFBlock(PDF, Rect(0, pos_y, 0, 2.5), Format(font_size=10, fill_color='#F0F0F099'))
    totales.text('Totales', bold=True, x=1, y=0.5, format_=F7)
    total_empleados = len(info_recibo['legajos'])
    totales.text(f'Cantidad de empleados: {total_empleados}', bold=True, x=12, y=0.5, format_=F7)

    total_rem2 = float_to_format_currency(total_rem)
    totales.text(f'Remunerativos {total_rem2}', bold=True, x=1, y=1.2, format_=F7)
    total_no_rem2 = float_to_format_currency(total_no_rem, 2)
    totales.text(f'No Remunerativos {total_no_rem2}', bold=True, x=7.3, y=1.2, format_=F7)
    total_desc2 = float_to_format_currency(total_desc)
    totales.text(f'Descuentos {total_desc2}', bold=True, x=14, y=1.2, format_=F7)

    neto = total_rem + total_no_rem - total_desc
    neto = float_to_format_currency(neto)
    totales.text(f'Neto a cobrar {neto}', bold=True, x=1, y=1.8, format_=F7)

    PDF.finish_page()
    PDF.save()
    return True, None


def draw_header(PDF: CanvasPDF):
    info_recibo = PDF.data
    log.info(f'Creando header en pagina {PDF.page}')
    # Estimar el alto que va a tener esto, necesito las actividades que son las que me pueden hacer variar esto
    # actividades
    actividad_principal = info_recibo.get('actividad_principal', {})
    actividades_secundarias = info_recibo.get('actividades_secundarias', [])
    total_act_secundarias = len(actividades_secundarias)
    initial_h = (
        1 +  # el header principal con el titulo
        0.4 +  # el nombre de la empresa
        0.6 +  # el domicilio de la empresa
        0.6 +  # la actividad principal
        (0.3 * total_act_secundarias)  # por cada actividad secundaria
    )
    # Agregar el bloque de headers izquiero
    header = CanvaPDFBlock(
        PDF,
        is_header=True,
        rect=Rect(0, 0, 0, initial_h),
        format_=Format(font_size=10, fill_color='#D0D0D0CC')
    )

    # Agregar contenido al header
    header.text('Hojas Móviles Libro Art. 52 Ley 20744', align='center', y=0.7, format_=F10, bold=True)
    col = [info_recibo['company_name'], info_recibo['domicilio']]
    header.text_column(col, start_x=0.4, start_y=1.3, format_=F7, bold=True)

    # Verificar que haya al menos una actividad principal
    if actividad_principal:
        apri_label = 'Actividad principal: '
        apri_name = actividad_principal.get('name', 'No especificada')

        # Mostrar la actividad principal
        header.text(apri_label, x=0.4, y=2.2, format_=F7, bold=True)
        header.text(apri_name, x=0.4 + 2.5, y=2.2, format_=F7)

        # Mostrar actividades secundarias si existen
        if actividades_secundarias:
            asec_label = 'Actividades secundarias:'
            header.text(asec_label, x=0.4, y=2.7, format_=F7, bold=True)

            for i, actividad in enumerate(actividades_secundarias):
                asec_name = actividad.get('name', 'No especificada')
                y_pos = 2.55 + (i + 0.5) * 0.3
                header.text(asec_name, x=0.4 + 3.19, y=y_pos, format_=F7)
    else:
        header.text(' Actividades no especificadas', x=0.4, y=2.2, format_=F7)

    # Agregar el bloque de headers derecho
    per_label = 'Periodo: '
    per_content = f'{info_recibo["tipo_liquidacion"]} {info_recibo["periodo"]}'
    cuit_label = 'CUIT: '
    cuit_content = info_recibo['cuit']
    col = [cuit_label, per_label]
    header.text_column(col, start_x=13, start_y=1.3, format_=F7, bold=True)
    header.text_column([cuit_content, per_content], start_x=14.4, start_y=1.3, format_=F7)

    return header


def draw_footer(PDF: CanvasPDF):
    log.info(f'Creando footer en pagina {PDF.page}')
    footer = CanvaPDFBlock(
        PDF, is_footer=True,
        rect=Rect(0, PDF.height-1, 0, 0.5), format_=Format(font_size=7, fill_color='#D0D0D0')
    )
    footer.text('Hojas Móviles Libro Art. 52 Ley 20744 -pagina {page}', align='center', y=0.3)
    return footer


def draw_empleado(PDF: CanvasPDF, empleado: dict, start_y, height):

    conceptos = empleado["conceptos_liquidados"]
    # Los conceptos se dividen por tipo
    remunerativos = [c for c in conceptos if c['tipo_concepto'] == 1]
    total_remu = len(remunerativos)
    no_remunerativos = [c for c in conceptos if c['tipo_concepto'] == 2]
    total_no_remu = len(no_remunerativos)
    descuentos = [c for c in conceptos if c['tipo_concepto'] == 3]
    total_desc = len(descuentos)
    # el total es igual al mayor de los tres
    total_c = max(total_remu, total_no_remu, total_desc)

    e_initial_h = (
        1 +  # el nombre del empleado
        0.5 +  # la información básica del empleado
        0.5 +  # la división automática del contrato
        0.5 +  # la información adicional del empleado
        (0.3 * total_c) +  # los conceptos
        1.2  # el neto a cobrar
    )

    empleado_block = CanvaPDFBlock(PDF, Rect(0, start_y, 0, e_initial_h), Format(font_size=7, fill_color='#F0F0F033'))
    name = f'{empleado["legajo"]} - {empleado["nombre"]}'
    y = 0.5
    empleado_block.text(name, bold=True, x=1, y=y)
    # Información básica del empleado
    lista = ['F. Ingreso', '', 'Remun. asignada']
    y = y + t9_line_sep + 0.1
    empleado_block.text_column(lista, start_x=1, start_y=y, line_sep=t9_line_sep, format_=F7, bold=True)
    lista = [empleado["fecha_ingreso"], empleado["fecha_ingreso_2"], empleado["basico"]]
    empleado_block.text_column(lista, start_x=3.5, start_y=y, line_sep=t9_line_sep, format_=F7)
    # División automática del contrato
    contrato_text = empleado["contrato"]
    # Si el contrato es muy largo, cortarlo al final sin puntos suspensivos
    if len(contrato_text) > 50:
        contrato_text = contrato_text[:55] + "..."

    lista = ['Estado civil', 'Puesto', 'Mod.Contrato']
    empleado_block.text_column(lista, start_x=6, start_y=y, line_sep=t9_line_sep, format_=F7, bold=True)
    lista = [empleado['estado_civil'], empleado["posicion"], contrato_text]
    empleado_block.text_column(lista, start_x=8, start_y=y, line_sep=t9_line_sep, format_=F7)
    # Información adicional del empleado
    lista = ['CUIL', 'Categoría', 'Seccion']
    y = 0.5 + t9_line_sep + 0.1
    empleado_block.text_column(lista, start_x=14.5, start_y=y, line_sep=t9_line_sep, format_=F7, bold=True)
    lista = [empleado["cuil"], empleado["categoria"], empleado["area"]]
    empleado_block.text_column(lista, start_x=16, start_y=y, line_sep=t9_line_sep, format_=F7)

    empleado_block.line(Rect(2, 2, 16, 1.9), line_with=2)

    y_titles = 2.3
    # Los tipos de conceptos son:
    # 1 Remunerativos
    # 2 No Remunerativos
    # 3 Descuentos

    def name_cant(cpt, max_length=30):
        """ Devuelve el nombre del concepto con la cantidad si la tiene """
        cantidad = cpt.get('cantidad')
        final = cpt['name']

        # Si el nombre es muy largo, cortarlo al final sin puntos suspensivos
        if len(final) > max_length:
            final = final[:max_length]

        if cantidad:
            final = f'{final} ({cantidad})'

        return final

    # REMUNERATIVOS

    # Buscar todos los conceptos remunerativos (tipo_concepto=1)
    empleado_block.text('Remunerativos', bold=True, x=0.3, y=y_titles, format_=F7)
    total_remu = sum([cpt['importe'] for cpt in remunerativos])
    empleado_block.text(float_to_format_currency(total_remu), x=5.5, y=y_titles, align='right', bold=True,  format_=F7)
    lista = [name_cant(cpt) for cpt in remunerativos]
    empleado_block.text_column(lista, start_x=0.3, start_y=y_titles + 0.5, line_sep=t9_line_sep, format_=F7)
    lista = [float_to_format_currency(cpt['importe'], include_currency=False) for cpt in remunerativos]
    empleado_block.text_column(lista, start_x=5.5, start_y=y_titles + 0.5, align='right', line_sep=t9_line_sep, format_=F7)

    # NO REMUNERATIVOS

    # Buscar todos los conceptos no remunerativos (tipo_concepto=2)
    empleado_block.text('No Remunerativos', bold=True, x=6, y=y_titles, format_=F7)
    total_no_remu = sum([cpt['importe'] for cpt in no_remunerativos])
    empleado_block.text(float_to_format_currency(total_no_remu), x=12, y=y_titles, align='right', bold=True, format_=F7)

    lista = [name_cant(cpt) for cpt in no_remunerativos]
    empleado_block.text_column(lista, start_x=6, start_y=y_titles + 0.5, line_sep=t9_line_sep, format_=F7)
    lista = [float_to_format_currency(cpt['importe'], include_currency=False) for cpt in no_remunerativos]
    empleado_block.text_column(lista, start_x=12, start_y=y_titles + 0.5, align='right', line_sep=t9_line_sep, format_=F7)

    # DESCUENTOS

    # Buscar todos los conceptos descuentos (tipo_concepto=3)
    empleado_block.text('Descuentos', bold=True, x=12.4, y=y_titles, format_=F7)
    total_desc = sum([cpt['importe'] for cpt in descuentos])
    empleado_block.text(float_to_format_currency(total_desc), x=18.7, y=y_titles, align='right', bold=True, format_=F7)

    lista = [name_cant(cpt) for cpt in descuentos]
    empleado_block.text_column(lista, start_x=12.4, start_y=y_titles + 0.5, line_sep=t9_line_sep, format_=F7)
    lista = [float_to_format_currency(cpt['importe'], include_currency=False) for cpt in descuentos]
    empleado_block.text_column(lista, start_x=18.7, start_y=y_titles + 0.5, align='right', line_sep=t9_line_sep, format_=F7)

    # NETO

    y_titles = e_initial_h - 2.4

    empleado_block.rectangle(Rect(1, y_titles+1.6, 5, 0.6), fill_color='#D0D0D0AA')
    neto_a_cobrar = float_to_format_currency(empleado["totales_liquidacion"]["neto_liquidacion"])
    empleado_block.text(f'Neto a cobrar   {neto_a_cobrar}', bold=True, x=1.2, y=y_titles+2, format_=F7)


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
