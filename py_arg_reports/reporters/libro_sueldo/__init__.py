import os
from py_arg_reports.reporters.libro_sueldo.info import get_recibo_info, get_info_final_for_libro_sueldo
from py_arg_reports.tools.base import CanvasPDF, CanvaPDFBlock, Format, Rect
from reportlab.lib.units import cm


def descargar_libro(json_data: dict, output_path: str, filename: str) -> str:
    """ Descarga el libro sueldo en formato PDF,
        Retorna error si lo hay
    """

    # recibo_info = get_recibo_info(json_data)
    # if recibo_info.get("error"):
    #     error_detail = recibo_info["error"]
    #     return error_detail

    # # Get info from recibo_info
    # info_recibo = get_info_final_for_libro_sueldo(recibo_info)

    # Cada liquidación va a tener su propia carpeta en download
    my_path = output_path
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    my_file_path = f'{my_path}{filename}.pdf'

    PDF = CanvasPDF(file_path=my_file_path, title='Libro Sueldo')

    # Agregar headers
    header_format = Format(font_size=14, color='#0000FF', fill_color='#FF000033')
    normal_format = Format(font_size=10)
    header_rect = Rect(0, 0, 0, 8)
    header = CanvaPDFBlock(PDF, header_rect, header_format)
    header.text('Hojas Móviles Libro Art. 52 Ley 20744', align='center', x=header.width / 2, y=1)
    header.text('Hecho con PayrollT', format_=Format(font_size=8), x=3, y=1.5)
    header.text('Nombre de la empresa', x=4, y=2, format_=normal_format)
    header.text('Direccion de la empresa', format_=normal_format, x=4, y=2.3)
    header.rectangle(Rect(0, 9, 19, 6), fill_color='#F0F0F0AA')
    header.line(Rect(10, 5, 11, 15), '#AACC00')
    header.line(Rect(12, 7, 10, 7), '#3300DDBB')

    PDF.canvas.showPage()
    PDF.canvas.save()

    PDF.export('py_arg_reports/reporters/libro_sueldo/samples/libro-sueldo-test.json')


if __name__ == '__main__':
    # Descargar el libro
    json_data = {}
    output_path = 'download/'
    filename = 'libro_sueldo'
    descargar_libro(json_data, output_path, filename)
    print(f'Libro sueldo descargado en {output_path}{filename}.pdf')
