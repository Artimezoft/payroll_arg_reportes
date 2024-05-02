import os

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

from py_arg_reports.reporters.libro_sueldo.base import my_base_libro_sueldo
from py_arg_reports.reporters.libro_sueldo.coords import draw_empleado, get_coordinates_for_libro_sueldo
from py_arg_reports.reporters.libro_sueldo.info import get_recibo_info, get_info_final_for_libro_sueldo


def descargar_libro(json_data: dict, output_path: str, filename: str) -> str:
    """ Descarga el libro sueldo en formato PDF,
        Retorna error si lo hay
    """
    resp = ''

    recibo_info = get_recibo_info(json_data)
    if recibo_info.get("error"):
        error_detail = recibo_info["error"]
        return error_detail

    # Cada liquidación va a tener su propia carpeta en download
    my_path = output_path
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    my_file_path = f'{my_path}{filename}.pdf'

    # Create a canvas
    c = canvas.Canvas(
        filename=my_file_path,
        pagesize=landscape(A4),
    )

    # Get info from recibo_info
    info_recibo = get_info_final_for_libro_sueldo(recibo_info)

    # Add the format to the file
    my_recibo_info = my_base_libro_sueldo(c)
    # c = my_recibo_info['canvas']

    # Get coordinates for recibo
    coordinates = get_coordinates_for_libro_sueldo(my_recibo_info=my_recibo_info)

    # --------------------------------------------------------------------------------------------
    # Loop through all the employees -------------------------------------------------------------
    # --------------------------------------------------------------------------------------------
    for legajo in info_recibo['legajos']:
        # Add the format to the file
        # TODO: Chequear porque debo hacerlo, antes funcionaba ok
        if legajo != info_recibo['legajos'][0]:
            my_recibo_info = my_base_libro_sueldo(c)

        # Draw the employee
        draw_empleado(
            c=c,
            coordinates=coordinates,
            info_recibo=info_recibo,
            legajo=legajo,
        )
        # Save the page
        c.showPage()

        # --------------------------------------------------------------------------------------------
        # End of Loop through all the employees ------------------------------------------------------
        # --------------------------------------------------------------------------------------------
    c.save()

    return resp
