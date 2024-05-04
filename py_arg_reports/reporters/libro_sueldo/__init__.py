import logging
import os
from py_arg_reports.reporters.libro_sueldo.info import get_recibo_info, get_info_final_for_libro_sueldo
from py_arg_reports.tools.base import CanvasPDF, CanvaPDFBlock, Format, Rect
from reportlab.lib.units import cm


log = logging.getLogger(__name__)


def descargar_libro(json_data: dict, output_path: str, filename: str) -> str:
    """ Descarga el libro sueldo en formato PDF,
        Retorna error si lo hay
    """

    recibo_info = get_recibo_info(json_data)
    if recibo_info.get("error"):
        error_detail = recibo_info["error"]
        return error_detail

    # Get info from recibo_info
    info_recibo = get_info_final_for_libro_sueldo(recibo_info)

    # Cada liquidación va a tener su propia carpeta en download
    my_path = output_path
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    my_file_path = f'{my_path}{filename}.pdf'
    log.info(f'Generando libro sueldo en {my_file_path}')

    # Mi PDF general donde voy a agregar los bloques
    PDF = CanvasPDF(file_path=my_file_path, title='Libro Sueldo', units=cm)

    # Agregar el bloque de headers
    header = CanvaPDFBlock(PDF, Rect(0, 0, 0, 4), Format(font_size=14, fill_color='#F0F0F0'))
    header.text('Hojas Móviles Libro Art. 52 Ley 20744', align='center', y=0.7)
    print(info_recibo['company_name'])
    header.text(info_recibo['company_name'], format_=Format(font_size=10), x=0.1, y=1)

    PDF.finish_page()
    PDF.save()

    PDF.export('py_arg_reports/reporters/libro_sueldo/samples/libro-sueldo-test.json')


if __name__ == '__main__':
    # En estas pruebas escupir los logs en la consola
    import sys
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    log.addHandler(handler)

    # Descargar el libro
    json_data = {}
    output_path = 'download/'
    filename = 'libro-sueldo'
    descargar_libro(json_data, output_path, filename)
    print(f'Libro sueldo descargado en {output_path}{filename}.pdf')
