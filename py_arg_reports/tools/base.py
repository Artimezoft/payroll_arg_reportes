
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas


class Rect:
    """ A rectangle, x, y, w, h """
    def __init__(self, x, y, w, h, units=cm):
        self.x = x * units
        self.y = y * units
        self.w = w * units
        self.h = h * units

    def __iter__(self):
        """ Para poder pasar los 4 como parametros: *rect """
        return iter([self.x, self.y, self.w, self.h])


class Format:
    """ A format for a block """
    def __init__(self, font='Helvetica', font_size=10, color=(0, 0, 0), fill_color=(0.9, 0.9, 0.9)):
        self.font = font
        self.font_size = font_size
        self.color = color
        self.fill_color = fill_color


class CanvasPDF:
    """ A PDF file from scratch """
    def __init__(self, file_path, title=None, pagesize=A4, units=cm, margin_x=1, margin_y=1):
        self.canvas = Canvas(file_path, pagesize=pagesize)
        self.pagesize = pagesize
        self.units = units
        self.width, self.height = pagesize
        self.margin_x = margin_x * units
        self.margin_y = margin_y * units
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


class CanvaPDFBlock:
    """ A Canvas PDF block with something, even pages"""
    def __init__(self, canvas: CanvasPDF, rect: Rect, format_: Format = None, with_rectangles=True):
        """ Inicializamos con coordenadas iniciales y ancho y alto si los hay"""
        # connect to the parent canvas
        # Our PDF canvas
        self.base_pdf = canvas
        # and the "real" canvas
        self.canvas = self.base_pdf.canvas
        # start_x, start_y: coordenadas iniciales para que los numeros internos sean siempre relativos
        # Un cero aqui significa que el bloque está en la esquina superior izquierda de este objeto, no de la página.
        if rect.x < self.base_pdf.margin_x:
            rect.x = self.base_pdf.margin_x
        self.start_x = rect.x * self.base_pdf.units
        if rect.y < self.base_pdf.margin_y:
            rect.y = self.base_pdf.margin_y
        self.start_y = rect.y * self.base_pdf.units
        # Yo podrìa no saber el ancho y alto, por eso los inicializo en None si es necesario
        max_width = self.base_pdf.width - (self.base_pdf.margin_x * 2)
        if rect.w is None or rect.w == 0:
            # Default es todo el ancho menos los márgenes
            rect.w = max_width
        elif rect.w < 0:
            # Si quiero un recorte del ancho (por ejemplo la mitad de la página)
            # uso negativos. -2 serìa 1/2
            rect.w = max_width / abs(rect.w)
        self.width = rect.w * self.base_pdf.units
        if rect.h is None:
            # Default es todo el alto menos los márgenes
            rect.h = self.base_pdf.height - (self.base_pdf.margin_y * 2)
        self.height = rect.h * self.base_pdf.units

        self.format = format_ if format_ else Format()

        # Tratar de mantener un puntero / cursor para saber donde estamos
        self.current_x = self.start_x
        self.current_y = self.start_y

        # Dibujar rectángulos del bloque
        if with_rectangles:
            self.rectangle(rect)

    def _relocate_rect(self, rect: Rect):
        """ Relocaliza el rectángulo en el canvas teniendo en cuenta el contexto general """
        rect.x = self.start_x + rect.x
        rect.y = self.start_y + rect.y
        return rect

    def rectangle(self, rect: Rect, color=None, fill_color=None, rounded=True):
        """ Dibuja un rectángulo en el canvas c """
        # reubicar el rectángulo en el canvas global
        rect = self._relocate_rect(rect)
        color = color if color else self.format.color
        self.canvas.setStrokeColorRGB(*color)
        fill_color = fill_color if fill_color else self.format.fill_color
        self.canvas.setFillColorRGB(*fill_color)
        if rounded:
            self.canvas.roundRect(*rect, radius=10)
        else:
            self.canvas.rect(*rect)

        # volver el puntero a donde inicia este bloque
        self.current_x = rect.x
        self.current_y = rect.y

    def line(self, rect: Rect, color=None):
        """ Dibujar una linea, en este caso Rect es un punto de inicio y otro de fin """
        rect = self._relocate_rect(rect)
        color = color or self.format.color
        self.canvas.setStrokeColorRGB(*color)
        self.canvas.line(*rect)
        # volver el puntero abajo de la linea
        self.current_x = rect.x
        self.current_y = rect.y

    def text(self, text, align='left', x=None, y=None, format_: Format = None):
        """ Dibuja un texto en el canvas c """
        x = x if x else self.current_x
        y = y if y else self.current_y

        # Pasar de coordenadas relativas a absolutas
        x = self.start_x + x
        y = self.start_y + y

        font = format_.font if format_ else self.format.font
        font_size = format_.font_size if format_ else self.format.font_size
        color = format_.color if format_ else self.format.color
        self.canvas.setFont(font, font_size)
        self.canvas.setFillColorRGB(*color)
        if align == 'left':
            self.canvas.drawString(x, y, text)
        elif align == 'right':
            self.canvas.drawRightString(x, y, text)
        elif align == 'center':
            # x aqui es el centro del texto
            self.canvas.drawCentredString(x, y, text)
        # actualizar el puntero
        self.current_x = x + self.canvas.stringWidth(text, font, font_size)
        # Move Y considering margin_h and this line
        self.current_y = y + font_size
