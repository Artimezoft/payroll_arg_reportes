import io

import xlsxwriter

from py_arg_reports.config import config_constants

DEFAULT_FONT = config_constants['EXCEL_FONT_FAMILY']
DEFAULT_FONT_SIZE = config_constants['EXCEL_FONT_SIZE']


def descarga_excel(info_dict: dict, sheet_name: str = 'Reporte'):
    """ Genera la información binaria para descargar un archivo excel.

        El formato de info_dict debe venir de esta manera:
        info_dict = {
            'headers': {
                'header1': {
                    'name': 'Es Texto',
                    'format': {'font_name': 'Arial', 'font_size': 8}
                },
                'header2': {
                    'name': 'Es Dinero',
                    'format': {'num_format': '$#,##0.00'},
                    'is_number': True,
                },
                'header3': {
                    'name': 'Es un número',
                    'format': {'num_format': '0.00'},
                    'is_number': True,
                },
            },
            'data': [
                {'header1': 'valor1', 'header2': 1320.10, 'header3': 0.123},
                {'header1': 'valor3', 'header2': 12312.10, 'header3': 2.23},
            ],
        }
    """
    # Creo el excel binario
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet(sheet_name)

    # Estilos -----------------------------------------
    # Negrita
    header_format = workbook.add_format({
        'font_name': DEFAULT_FONT,
        'font_size': DEFAULT_FONT_SIZE,
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#D7E4BC',
        'border': 1,
    })

    # Formato de celdas
    cell_format = workbook.add_format()
    cell_format.set_font(DEFAULT_FONT)
    cell_format.set_font_size(DEFAULT_FONT_SIZE)
    base_dict_format = {
        'font_name': DEFAULT_FONT,
        'font_size': DEFAULT_FONT_SIZE,
    }
    # -------------------------------------------------

    # Algo de formato
    worksheet.freeze_panes(1, 1)

    # Formato de headers
    header_idx = 0
    cell_formats = []
    for header in info_dict['headers']:
        worksheet.write(0, header_idx, info_dict['headers'][header]['name'], header_format)
        new_format = {**base_dict_format, **info_dict['headers'][header].get('format', {})}
        cell_formats.append(workbook.add_format(new_format))
        header_idx += 1

    # Formato de datos
    for row, data in enumerate(info_dict['data'], 1):
        for col, header in enumerate(info_dict['headers']):
            cell_value = data.get(header, '')
            if 'is_number' in info_dict['headers'][header]:
                try:
                    worksheet.write_number(row, col, cell_value, cell_formats[col])
                except TypeError as e:
                    raise ValueError(f'Error del valor "{cell_value}" la celda [{row+1}, {col+1}]: {e}')
            else:
                worksheet.write(row, col, cell_value, cell_formats[col])

    workbook.close()
    # Retrieve the binary data from BytesIO object
    excel_data = output.getvalue()
    return excel_data
