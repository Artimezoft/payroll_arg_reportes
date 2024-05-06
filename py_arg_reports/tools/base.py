from copy import deepcopy
from py_arg_reports.logs import get_logger
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas


log = get_logger(__name__)


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

    def copy(self):
        return Rect(self.x, self.y, self.w, self.h, units=self.units)


class Format:
    """ A format for a block """
    def __init__(
            self,
            font='Helvetica', font_bold='Helvetica-Bold',
            font_size=10,
            color='#000000', fill_color='#F0F0F0'
    ):
        self.font = font
        self.font_bold = font_bold
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

    def copy(self):
        return Format(
            font=self.font, font_bold=self.font_bold,
            font_size=self.font_size,
            color=self.color, fill_color=self.fill_color
        )


class CanvasPDF:
    """ A PDF file from scratch """
    def __init__(
            self, file_path, title=None,
            pagesize=A4, units=cm,
            margin_x=1, margin_y=1,
            data={},  # datos generales con los que se construye el PDF
    ):
        self.canvas = Canvas(file_path, pagesize=pagesize, bottomup=False)
        self.pagesize = pagesize
        self.units = units
        self.data = data
        self.width_raw, self.height_raw = pagesize
        self.width = self.width_raw / units
        self.height = self.height_raw / units
        self.margin_x = margin_x
        self.margin_y = margin_y
        # Se van agregando bloques y algunos se pasan de la pagina y empieza otra nueva
        # entonces giuardo registro de donde voy para seguir de donde deje
        self.last_y = margin_y
        # llevo registro de la pagina actual
        self.page = 1
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
        # los bloques de header y de footer se guardan para crear en cada pagina
        self.header_block = None
        self.footer_block = None

    def __str__(self):
        w = round(self.width, 2)
        h = round(self.height, 2)
        mw = round(self.margin_x, 2)
        mh = round(self.margin_y, 2)
        return f'CanvasPDF: ({w} [{mw}] x {h} [{mh}])'

    def finish_page(self):
        """ Terminar la página actual """
        self.canvas.showPage()

    def save(self):
        """ Guardar el PDF """
        self.canvas.save()


class CanvaPDFBlock:
    """ A Canvas PDF block with something, even pages"""

    def __init__(
            self, canvas: CanvasPDF,
            rect: Rect, format_: Format = None,
            is_header=False,  # Si es un header lo guardo
            is_footer=False,  # Si es un footer lo guardo
            is_redraw=False,
            with_rectangles=True
    ):
        """ Inicializamos con coordenadas iniciales y ancho y alto si los hay"""
        # connect to the parent canvas
        # Our PDF canvas
        self.base_pdf = canvas
        self.original_rect = rect.copy() if rect else None
        self.original_format = format_.copy() if format_ else None
        self.history = []  # changes history to re draw
        if is_header:
            self.base_pdf.header_block = self
        if is_footer:
            self.base_pdf.footer_block = self
        self.is_header = is_header
        self.is_footer = is_footer

        # and the "real" canvas
        self.canvas = self.base_pdf.canvas

        # Si este bloque pasa la pagina actual, terminar la pagina
        # al footer lo perdonamos
        ignore_end = is_footer or is_redraw
        if not ignore_end and (rect.y + rect.h > self.base_pdf.height - self.base_pdf.margin_y):
            log.info(f'Block is going to pass the page {self.base_pdf.page}, finishing page')
            self.base_pdf.finish_page()
            # Recomenzar Y
            rect.y = self.base_pdf.margin_y
            self.start_y = rect.y
            self.base_pdf.page += 1
            # re draw header and footer
            if self.base_pdf.header_block:
                log.debug(f'Redrawing HEADER for page {self.base_pdf.page}')
                self.base_pdf.header_block.re_draw()
                rect.y += self.base_pdf.header_block.original_rect.h + 0.1
            if self.base_pdf.footer_block:
                log.debug(f'Redrawing FOOTER for page {self.base_pdf.page}')
                self.base_pdf.footer_block.re_draw()

        # La coordenada Y empieza abajo de todo de la pagina si no ponemos bottomup=False
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

        # Dibujar rectángulos del bloque
        self.with_rectangles = with_rectangles
        if with_rectangles:
            self.rectangle(
                rect, color=self.format.color,
                fill_color=self.format.fill_color,
                move_start=False
            )
        # Como no se si pase pagina y se creo otra guardo registro del Y maximo donde termine
        # No tener en cuenta si estoy dibujando el footer!
        if not is_footer:
            self.base_pdf.last_y = self.start_y + self.height

    def _rect_to_units(self, rect, move_start=True, move_end=False):
        """ Convierte un rectángulo relativo a uno absoluto """
        # move to start coords
        u = self.base_pdf.units
        x2 = rect.x
        y2 = rect.y
        if move_start:
            # El rectangulo de bloque inicial ya tiene esto considerado
            x2 += self.start_x
            y2 += self.start_y

        x2 = x2 * u
        y2 = y2 * u

        w2 = rect.w or 0
        h2 = rect.h or 0

        if move_end:
            # Esto es una linea, los parametros del final son x2 e y2
            w2 += self.start_x
            h2 += self.start_y

        w2 = w2 * u
        h2 = h2 * u

        # Si bottomup fuera True necesitaria algo asi
        # page_h = self.base_pdf.height * u
        # y3 = page_h - y2
        r = Rect(x2, y2, w2, h2, units=self.base_pdf.units)
        return r

    def rectangle(self, rect: Rect, color=None, fill_color=None, line_width=0.5, rounded=True, move_start=True):
        """ Dibuja un rectángulo en el canvas c """
        log.debug(f'Drawing rectangle at page {self.base_pdf.page}')
        self.history.append(
            {
                'type': 'rectangle',
                'rect': rect.copy(),
                'color': color,
                'fill_color': fill_color,
                'line_width': line_width,
                'rounded': rounded,
                'move_start': move_start,
            }
        )
        # reubicar el rectángulo en el canvas globalself.start_y + rect.y
        rect2 = self._rect_to_units(rect, move_start=move_start)

        color = color if color else self.format.color
        has_alpha = len(color) == 9
        self.canvas.setStrokeColor(HexColor(color, hasAlpha=has_alpha))

        fill_color = fill_color if fill_color else self.format.fill_color
        has_alpha = len(fill_color) == 9
        self.canvas.setFillColor(HexColor(fill_color, hasAlpha=has_alpha))
        self.canvas.setLineWidth(line_width)
        if rounded:
            self.canvas.roundRect(*rect2, radius=3, stroke=1, fill=1)
        else:
            self.canvas.rect(*rect2, stroke=1, fill=1)

    def line(self, rect: Rect, color=None, line_with=1):
        """ Dibujar una linea, en este caso Rect es un punto de inicio y otro de fin """
        log.info(f'Drawing line {rect} at page {self.base_pdf.page}')
        self.history.append(
            {
                'type': 'line',
                'rect': rect.copy(),
                'color': color,
                'line_with': line_with,
            }
        )
        rect2 = self._rect_to_units(rect, move_end=True)
        color = color or self.format.color
        self.canvas.setStrokeColor(HexColor(color))
        # define the border size
        self.canvas.setLineWidth(line_with)
        self.canvas.line(*rect2)

    def text(self, text, x=0, y=0, align='left', bold=False, format_: Format = None):
        """ Dibuja un texto en el canvas c """
        if not text:
            text = ''
        log.debug(f'Drawing text [{text[:10]}] at ({x}, {y}) - page {self.base_pdf.page}')
        if not text:
            return

        self.history.append(
            {
                'type': 'text',
                'text': text,
                'x': x,
                'y': y,
                'align': align,
                'bold': bold,
                'format_': format_,
            }
        )

        # Puede haber valores dinamicos. Por ahora la página
        # Esto podria ser mejor si hay mas valores
        text = text.replace('{page}', str(self.base_pdf.page))

        # Si es centrado y no me da x propongo la mitad del ancho de este bloque
        if align == 'center' and x == 0:
            x = self.width / 2
        # Pasar de coordenadas relativas a absolutas
        u = self.base_pdf.units
        x2 = self.start_x + x
        y2 = self.start_y + y

        x2 = x2 * u
        y2 = y2 * u
        # Si bottomup fuera True necesitaria algo asi
        # y2 = (self.base_pdf.height * u) - y2

        format_ = format_ or self.format
        font = format_.font_bold if bold else self.format.font

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

    def text_column(self, text_list, line_sep=0.4, start_x=0, start_y=0, align='left', bold=False, format_: Format = None):
        """ Escribir una columna de textos """
        for i, text in enumerate(text_list):
            self.text(text, x=start_x, y=start_y + (line_sep * i), align=align, format_=format_, bold=bold)

    def re_draw(self):
        """ Redibujar el bloque """
        log.info(f'Redraw at page {self.base_pdf.page}')
        block = CanvaPDFBlock(
            canvas=self.base_pdf,
            rect=self.original_rect.copy(), format_=self.original_format.copy(),
            is_header=False, is_footer=False,  # ya lo son
            is_redraw=True,
            with_rectangles=self.with_rectangles,
        )
        # apply history
        history_orig = deepcopy(self.history)
        for h in history_orig:
            type_ = h.pop('type', None)
            log.debug(f'Redrawing {type_} at page {self.base_pdf.page}')
            if type is None:
                err = f'No type in history: {h}'
                log.error(err)
                raise Exception(err)
            if type_ == 'rectangle':
                block.rectangle(**h)
            elif type_ == 'line':
                block.line(**h)
            elif type_ == 'text':
                block.text(**h)
