import json
import logging
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas


log = logging.getLogger(__name__)


class Rect:
    """ A rectangle, x, y, w, h """
    def __init__(self, x, y, w, h, units=cm):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.units = units

    def __iter__(self):
        """ Para poder pasar los 4 como parametros: *rect """
        return iter([self.x, self.y, self.w, self.h])

    def __str__(self):
        x = round(self.x / self.units, 2)
        y = round(self.y / self.units, 2)
        w = round(self.w / self.units, 2) if self.w else '-'
        h = round(self.h / self.units, 2) if self.h else '-'
        return f'Rect({x}, {y}, {w}, {h})'

    def as_dict(self, units=False):
        x = round(self.x, 2) if not units else round(self.x / self.units, 2)
        y = round(self.y, 2) if not units else round(self.y / self.units, 2)
        w = round(self.w, 2) if not units else round(self.w / self.units, 2)
        h = round(self.h, 2) if not units else round(self.h / self.units, 2)
        return {'x': x, 'y': y, 'w': w, 'h': h, 'units': round(self.units, 2)}


class Format:
    """ A format for a block """
    def __init__(self, font='Helvetica', font_size=10, color='#000000', fill_color='#F0F0F0'):
        self.font = font
        self.font_size = font_size
        # Los colores son como los de HTML #RRGGBBAA, despues los transformamos al pintar
        self.color = color
        self.fill_color = fill_color

    def __str__(self):
        return f'Format(font={self.font}, font_size={self.font_size}, color={self.color}, fill_color={self.fill_color})'

    def as_dict(self):
        return {
            'font': self.font,
            'font_size': self.font_size,
            'color': self.color,
            'fill_color': self.fill_color,
        }


class CanvasPDF:
    """ A PDF file from scratch """
    def __init__(self, file_path, title=None, pagesize=A4, units=cm, margin_x=1, margin_y=1):
        self.canvas = Canvas(file_path, pagesize=pagesize)
        self.pagesize = pagesize
        self.units = units
        self.width_raw, self.height_raw = pagesize
        self.width = self.width_raw / units
        self.height = self.height_raw / units
        self.margin_x = margin_x
        self.margin_y = margin_y
        if title:
            # Define a PDF title
            self.canvas.setTitle(title)
        # Define a PDF author
        self.canvas.setAuthor('PayrollT')
        # Define a PDF subject
        self.canvas.setSubject('Software de Liquidación de Sueldos PayrollT')
        # Define a PDF creator
        self.canvas.setCreator('PayrollT creations')
        # Define a PDF producer
        self.canvas.setProducer('PayrollT productions')
        # Guardar registro de todo para depurar y definir un formato para importar
        self.content = []
        # registrar este inicio
        self.content.append(
            {
                'type': 'init',
                'width': round(self.width, 2),
                'height': round(self.height, 2),
                'margin_x': self.margin_x,
                'margin_y': self.margin_y,
                'pagesize': list(pagesize),
                'units': round(units, 2),
            }
        )

    def __str__(self):
        w = round(self.width, 2)
        h = round(self.height, 2)
        mw = round(self.margin_x, 2)
        mh = round(self.margin_y, 2)
        return f'CanvasPDF: ({w} [{mw}] x {h} [{mh}])'

    def export(self, file_path):
        """ Exportar el contenido del PDF """
        f = open(file_path, 'w')
        try:
            f.write(json.dumps(self.content, indent=4))
        except Exception as e:
            log.error(f'Error exporting PDF content: {e}\n{self.content}')
            raise e
        else:
            log.info(f'PDF content exported to {file_path}')
        f.close()


class CanvaPDFBlock:
    """ A Canvas PDF block with something, even pages"""

    def __init__(self, canvas: CanvasPDF, rect: Rect, format_: Format = None, with_rectangles=True):
        """ Inicializamos con coordenadas iniciales y ancho y alto si los hay"""
        # connect to the parent canvas
        # Our PDF canvas
        self.base_pdf = canvas
        # and the "real" canvas
        self.canvas = self.base_pdf.canvas

        self.base_pdf.content.append(
            {
                'type': 'PDFBlock_before_init',
                'rect': rect.as_dict(),
                'format': format_.as_dict() if format_ else None,
            }
        )
        # La coordenada Y empieza abajo de todo de la pagina
        # y se va moviendo hacia arriba
        # asi que dejo a los usuarios sean normales y lidiamos aca con las coordenadas
        # start_x, start_y: coordenadas iniciales para que los numeros internos sean siempre relativos
        # Un cero aqui significa que el bloque está en la esquina superior izquierda de este objeto, no de la página.
        if rect.x < self.base_pdf.margin_x:
            rect.x = self.base_pdf.margin_x
        self.start_x = rect.x
        if rect.y < self.base_pdf.margin_y:
            rect.y = self.base_pdf.margin_y
        self.start_y = rect.y
        # Yo podrìa no saber el ancho y alto, por eso los inicializo en None si es necesario
        max_width = self.base_pdf.width - (self.base_pdf.margin_x * 2)
        if rect.w is None or rect.w == 0 or rect.w > max_width:
            # Default es todo el ancho menos los márgenes
            rect.w = max_width
        elif rect.w < 0:
            # Si quiero un recorte del ancho (por ejemplo la mitad de la página)
            # uso negativos. -2 serìa 1/2
            rect.w = max_width / abs(rect.w)
        self.width = rect.w
        if rect.h is None:
            # Default es todo el alto menos los márgenes
            rect.h = self.base_pdf.height - (self.base_pdf.margin_y * 2)
        self.height = rect.h

        self.format = format_ if format_ else Format()

        # Registrar este bloque
        self.base_pdf.content.append(
            {
                'type': 'PDFBlock_after_init',
                'rect': rect.as_dict(),
                'format': self.format.as_dict(),
            }
        )
        # Dibujar rectángulos del bloque
        if with_rectangles:
            self.rectangle(
                rect, color=self.format.color,
                fill_color=self.format.fill_color,
                move_start=False
            )

    def _rect_to_units(self, rect, move_start=True):
        """ Convierte un rectángulo relativo a uno absoluto """
        # move to start coords
        u = self.base_pdf.units
        x2 = rect.x
        y2 = rect.y + 10
        if move_start:
            # El rectangulo de bloque inicial ya tiene esto considerado
            x2 += self.start_x
            y2 += self.start_y

        x2 = x2 * u
        y2 = y2 * u

        w = rect.w * u if rect.w else 0
        h = rect.h * u if rect.h else 0

        page_h = self.base_pdf.height * u
        y3 = page_h - y2
        print(f'y: {rect.y}::{y2/u} y3: {y3/u}, page height: {self.base_pdf.height}')
        r = Rect(x2, y3, w, h, units=self.base_pdf.units)
        print(r)
        return r

    def rectangle(self, rect: Rect, color=None, fill_color=None, rounded=True, move_start=True):
        """ Dibuja un rectángulo en el canvas c """
        # reubicar el rectángulo en el canvas globalself.start_y + rect.y
        rect2 = self._rect_to_units(rect, move_start=move_start)
        self.base_pdf.content.append(
            {
                'type': 'rectangle',
                'rect1': rect.as_dict(),
                'rect2': rect2.as_dict(units=True),
                'color': color,
                'fill_color': fill_color,
                'rounded': rounded,
            }
        )

        color = color if color else self.format.color
        has_alpha = len(color) == 9
        self.canvas.setStrokeColor(HexColor(color, hasAlpha=has_alpha))

        fill_color = fill_color if fill_color else self.format.fill_color
        has_alpha = len(fill_color) == 9
        self.canvas.setFillColor(HexColor(fill_color, hasAlpha=has_alpha))

        print(f'final rect {rect2.as_dict(units=True)}')
        if rounded:
            # self.canvas.roundRect(rect2.x, rect2.y, rect2.w, rect2.h, radius=3, stroke=1, fill=1)
            self.canvas.roundRect(*rect2, radius=3, stroke=1, fill=1)
        else:
            self.canvas.rect(*rect2, stroke=1, fill=1)

    def line(self, rect: Rect, color=None):
        """ Dibujar una linea, en este caso Rect es un punto de inicio y otro de fin """
        rect2 = self._rect_to_units(rect)
        self.base_pdf.content.append(
            {
                'type': 'line',
                'rect1': rect.as_dict(),
                'rect2': rect2.as_dict(units=True),
                'color': color,
            }
        )
        color = color or self.format.color
        self.canvas.setStrokeColor(HexColor(color))
        self.canvas.line(*rect2)

    def text(self, text, x, y, align='left', format_: Format = None):
        """ Dibuja un texto en el canvas c """
        # Pasar de coordenadas relativas a absolutas
        u = self.base_pdf.units
        x2 = self.start_x + x
        y2 = self.start_y + y

        x2 = x2 * u
        y2 = y2 * u
        y2 = (self.base_pdf.height * u) - y2
        self.base_pdf.content.append(
            {
                'type': 'text',
                'text': text,
                'align': align,
                'x': round(x, 2),
                'x2': round(x2/u, 2),
                'y': round(y, 2),
                'y2': round(y2/u, 2),
            }
        )

        font = format_.font if format_ else self.format.font
        font_size = format_.font_size if format_ else self.format.font_size
        color = format_.color if format_ else self.format.color
        self.canvas.setFont(font, font_size)
        self.canvas.setFillColor(HexColor(color))
        if align == 'left':
            self.canvas.drawString(x2, y2, text)
        elif align == 'right':
            self.canvas.drawRightString(x2, y2, text)
        elif align == 'center':
            # x aqui es el centro del texto
            self.canvas.drawCentredString(x2, y2, text)
