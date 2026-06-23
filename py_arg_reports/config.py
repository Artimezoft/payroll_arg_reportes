
from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def _register_pdf_fonts() -> tuple[str, str]:
    fonts_path = Path(__import__('reportlab').__file__).resolve().parent / 'fonts'
    regular_font_path = fonts_path / 'Vera.ttf'
    bold_font_path = fonts_path / 'VeraBd.ttf'

    if regular_font_path.exists() and bold_font_path.exists():
        pdfmetrics.registerFont(TTFont('Vera', str(regular_font_path)))
        pdfmetrics.registerFont(TTFont('VeraBd', str(bold_font_path)))
        return 'Vera', 'VeraBd'

    return 'Helvetica', 'Helvetica-Bold'


font_family, font_family_bold = _register_pdf_fonts()

config_constants = {
    # Recibos
    'FONT_FAMILY': font_family,
    'FONT_FAMILY_BOLD': font_family_bold,
    'FONT_SIZE_MAIN': 9,
    'FONT_SIZE_HEADER': 12,
    'FONT_SIZE_BODY': 8,
    'FONT_SIZE_SMALL': 7,

    # Excel
    'EXCEL_FONT_FAMILY': 'Arial',
    'EXCEL_FONT_SIZE': 8,
}
