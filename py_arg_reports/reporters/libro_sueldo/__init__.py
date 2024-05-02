import os
from py_arg_reports.reporters.libro_sueldo.info import get_recibo_info, get_info_final_for_libro_sueldo
from py_arg_reports.tools.base import CanvasPDF, CanvaPDFBlock, Format, Rect


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
    header_format = Format(font_size=14)
    normal_format = Format(font_size=10)
    header_rect = Rect(0, 0, PDF.width, 5)
    header = CanvaPDFBlock(PDF, header_rect, header_format)
    header.text('Hojas Móviles Libro Art. 52 Ley 20744', align='center', x=header.width / 2)
    header.text('Hecho con PayrollT', format_=Format(font_size=8))
    header.text('Nombre de la empresa', y=2, format_=normal_format)
    header.text('Direccion de la empresa', format_=normal_format)

    PDF.canvas.showPage()
    PDF.canvas.save()


if __name__ == '__main__':
    # Descargar el libro
    json_data = {}
    output_path = 'download/'
    filename = 'libro_sueldo'
    descargar_libro(json_data, output_path, filename)
    print(f'Libro sueldo descargado en {output_path}{filename}.pdf')
