import json
import os
import tempfile

from PyPDF2 import PdfReader

from py_arg_reports.reporters.recibo_sueldo.base import ReciboDownloader


class TestDownloadRecibo:
    """ Testing para Descargar Recibos
    """
    @classmethod
    def setup_class(cls):
        # Specify the path where the temporary folder should be created
        temp_folder_path = './tests/temp/'
        # Create a temporary folder for testing in the specified path
        cls.temp_folder = tempfile.mkdtemp(dir=temp_folder_path)
        if cls.temp_folder[-1] != '/':
            cls.temp_folder += '/'

        with open('./py_arg_reports/test_cases/liquidacion_completa.json', 'r', encoding='utf-8') as f:
            cls.long_json = json.load(f)

        with open('./py_arg_reports/test_cases/liquidacion_corta.json', 'r', encoding='utf-8') as f:
            cls.short_json = json.load(f)

        # Load fixture with contributions and excluded concepts
        with open('./py_arg_reports/test_cases/liquidacion_con_contribuciones.json', 'r', encoding='utf-8') as f:
            cls.contributions_json = json.load(f)

    def setup_method(self):
        self.empty_json = {}
        self.key_missing_json = [{
            'empleado': 'Juan',
            'empresa': 'Empresa',
            'conceptos_liquidados': 'Conceptos',
            'liquidacion': 'Liquidacion',
            }]

    def extract_pdf_text(self, file_path):
        """ Helper method to extract text from all pages of a PDF """
        text_content = ""
        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)
            for page in pdf.pages:
                text_content += page.extract_text()
        return text_content

    @classmethod
    def teardown_class(cls):
        # Clean up: Delete the temporary folder and its contents
        if os.path.exists(cls.temp_folder):
            for root, dirs, files in os.walk(cls.temp_folder, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            os.rmdir(cls.temp_folder)

    def test_descarga_recibo_1(self):
        """ Prueba la descarga del archivo
        """
        recibo_downloader = ReciboDownloader(
            json_data=self.short_json,
            output_path=self.temp_folder,
            filename='recibo_prueba_1',
        )
        full_path, error = recibo_downloader.descargar_recibo()
        assert error is None

        # Check if the file exists
        assert os.path.exists(full_path)

        # Check the number of pages in the PDF file
        with open(full_path, 'rb') as file:
            # pdf_reader = PyPDF2.PdfFileReader(f)
            pdf = PdfReader(file)
            num_sheets = len(pdf.pages)

        assert num_sheets == 3

    def test_descarga_recibo_2(self):
        """ Prueba la descarga del archivo full
        """
        recibo_downloader = ReciboDownloader(
            json_data=self.long_json,
            output_path=self.temp_folder,
            filename='recibo_prueba_2',
        )
        full_path, error = recibo_downloader.descargar_recibo()

        assert error is None

        # Check if the file exists
        assert os.path.exists(full_path)

        # Check the number of pages in the PDF file
        with open(full_path, 'rb') as file:
            # pdf_reader = PyPDF2.PdfFileReader(f)
            pdf = PdfReader(file)
            num_sheets = len(pdf.pages)

        assert num_sheets == 25

    def test_descarga_recibo_3_poc(self):
        """ Prueba el nuevo enfoque abstracto con layout class-based (base_version=3). """
        recibo_downloader = ReciboDownloader(
            json_data=self.short_json,
            output_path=self.temp_folder,
            filename='recibo_prueba_3_poc',
            base_version=3,
        )
        full_path, error = recibo_downloader.descargar_recibo()

        assert error is None
        assert os.path.exists(full_path)

        with open(full_path, 'rb') as file:
            pdf = PdfReader(file)
            num_sheets = len(pdf.pages)

        assert num_sheets == 3

    def test_descarga_empty_json(self):
        """ Prueba la descarga del archivo para un json vacío
        """
        recibo_downloader = ReciboDownloader(
            json_data=self.empty_json,
            output_path=self.temp_folder,
            filename='recibo_prueba_3',
        )
        full_path, error = recibo_downloader.descargar_recibo()

        assert error == 'No se puede descargar el recibo, no hay datos'

    def test_key_missing_json(self):
        """ Prueba la descarga del archivo para un json sin la key 'results'
        """
        recibo_downloader = ReciboDownloader(
            json_data=self.key_missing_json,
            output_path=self.temp_folder,
            filename='recibo_prueba_5',
        )
        _, error = recibo_downloader.descargar_recibo()

        assert error == 'No se puede descargar el recibo, no se observa totales_liquidacion en los datos'

    def test_descarga_con_contribuciones(self):
        """ Test PDF generation with contributions (tipo_concepto: 4) """
        recibo_downloader = ReciboDownloader(
            json_data=self.contributions_json,
            output_path=self.temp_folder,
            filename='recibo_contribuciones_test',
        )
        full_path, error = recibo_downloader.descargar_recibo()

        assert error is None
        assert os.path.exists(full_path)

        # Extract text from PDF
        pdf_text = self.extract_pdf_text(full_path)

        # Verify contributions appear in PDF
        assert "Contribución Obra Social" in pdf_text, "Contribution concept should appear in PDF"
        assert "Contribución Sindical" in pdf_text, "Contribution concept should appear in PDF"

        # Check contribution amounts are displayed
        assert "2.500,50" in pdf_text, "Contribution amount should appear in PDF"  # Formatted currency for contribution 1
        assert "1.200,75" in pdf_text, "Contribution amount should appear in PDF"  # Formatted currency for contribution 2

    def test_excluded_concepts_not_in_pdf(self):
        """ Test that excluded concepts (CREFIS) don't appear in PDF """
        recibo_downloader = ReciboDownloader(
            json_data=self.contributions_json,
            output_path=self.temp_folder,
            filename='recibo_excluded_test',
        )
        full_path, error = recibo_downloader.descargar_recibo()

        assert error is None
        assert os.path.exists(full_path)

        # Extract text from PDF
        pdf_text = self.extract_pdf_text(full_path)

        # Verify CREFIS concept does not appear in PDF
        assert "CREFIS" not in pdf_text, "CREFIS concept should be excluded from PDF"
        assert "CREFIS - Excluido" not in pdf_text, "CREFIS concept name should be excluded from PDF"

    def test_total_contribuciones_calculation(self):
        """ Test that total contributions are calculated and displayed correctly """
        recibo_downloader = ReciboDownloader(
            json_data=self.contributions_json,
            output_path=self.temp_folder,
            filename='recibo_total_contribuciones_test',
        )
        full_path, error = recibo_downloader.descargar_recibo()

        assert error is None
        assert os.path.exists(full_path)

        # Extract text from PDF
        pdf_text = self.extract_pdf_text(full_path)

        # Total should be 2500.50 + 1200.75 = 3701.25
        # In formatted currency: 3.701,25
        assert "3.701,25" in pdf_text, "Total contributions amount should appear in PDF"

    def test_multiple_contributions_rendering(self):
        """ Test that multiple contributions render correctly in columns """
        # Create additional contributions fixture if needed for this test
        recibo_downloader = ReciboDownloader(
            json_data=self.contributions_json,
            output_path=self.temp_folder,
            filename='recibo_multiple_contrib_test',
        )
        full_path, error = recibo_downloader.descargar_recibo()

        assert error is None
        assert os.path.exists(full_path)

        # Check that PDF is generated successfully with multiple contributions
        with open(full_path, 'rb') as file:
            pdf = PdfReader(file)
            num_sheets = len(pdf.pages)

        # Should have at least 1 page
        assert num_sheets >= 1
