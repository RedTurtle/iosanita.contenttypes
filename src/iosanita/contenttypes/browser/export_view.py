from datetime import datetime
from io import BytesIO
from io import StringIO
from iosanita.contenttypes import _
from plone import api
from Products.Five.browser import BrowserView
from weasyprint import HTML
from zExceptions import BadRequest
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import csv
import importlib.resources
import logging
import re


logger = logging.getLogger(__name__)

fontools_logger = logging.getLogger("fontTools.subset")
fontools_logger.setLevel(logging.WARNING)


class IExportViewTraverser(IPublishTraverse):
    """
    Marker interface for Download views
    """


@implementer(IExportViewTraverser)
class ExportViewTraverser(BrowserView):
    pass


class IExportViewDownload(IPublishTraverse):
    pass


@implementer(IExportViewDownload)
class ExportViewDownload(BrowserView):
    """
    @@download view that need to be called over a view that implements IExportViewTraverser

    """

    with_footer = True

    def __init__(self, context, request):
        super().__init__(context, request)
        self.export_type = "csv"

    def publishTraverse(self, request, name):
        """
        e.g.
        .../it/bandi/avvisi/view-name/@@download/csv?xxx=yyy
        """
        self.export_type = name or "csv"
        return self

    def __call__(self):
        """ """
        if self.export_type not in ["csv", "pdf", "html"]:
            raise BadRequest(
                api.portal.translate(
                    _(
                        "invalid_export_type",
                        default="Invalid export type: ${export_type}",
                        mapping={"export_type": self.export_type},
                    )
                )
            )
        data = self.get_data()
        if self.export_type == "csv":
            # default per locales di riferimento (perr l'encoding, al momento, lasciamo
            # il generico utf-8 con BOM che potrebbe funzionare per tutti,
            # MS Excel incluso)
            lang = api.portal.get_current_language(self.context)
            if lang == "it":
                sep = ";"
            else:
                sep = ","
            return self.get_csv(data, sep=sep)
        elif self.export_type == "pdf":
            return self.get_pdf(data)
        elif self.export_type == "html":
            return self.get_html_for_pdf(data)
        return resp_data

    def get_filename(self):
        """
        Return the filename for the CSV export.
        """
        now = datetime.now().strftime("%Y_%m_%d_%H_%M")
        return f"export_{now}.{self.export_type}"

    def get_csv(self, data, encoding="utf-8-sig", sep=","):
        """
        Generate CSV data from the provided data.
        """
        # 1. Crea uno StringIO per il CSV
        csv_buffer = StringIO()
        # 2. Aggiungi l'header per il separatore (specifico per Excel)
        # In Libreoffice viene aggiunta una riga, per ora evitiamo
        # csv_buffer.write(f"sep={sep}\n")
        # 3. Scrittura dei dati CSV
        columns = self.get_columns(data)
        csv_writer = csv.writer(csv_buffer, delimiter=sep, quoting=csv.QUOTE_ALL)
        csv_writer.writerow([c["title"] for c in columns])
        for item in data:
            csv_writer.writerow(self.format_row(item))
        # 4. Prepara i bytes con BOM (UTF-8-sig)
        csv_data = csv_buffer.getvalue()
        if encoding == "utf-8-sig":
            csv_bytes = b'\xef\xbb\xbf' + csv_data.encode('utf-8')  # Aggiunge BOM
        else:
            csv_bytes = cvs_data.encode(encoding)
        # 5. Crea la risposta con gli header corretti
        response = self.request.response
        response.setHeader("Content-Disposition", f"attachment;filename={self.get_filename()}")
        response.setHeader("Content-Type", f"text/csv; charset={encoding}")
        return csv_bytes

    def get_pdf(self, data):
        html_str = self.get_html_for_pdf(data=data)
        pdf_file = BytesIO()
        HTML(string=html_str).write_pdf(pdf_file)
        pdf_file.seek(0)
        # 5. Crea la risposta con gli header corretti
        response = self.request.response
        response.setHeader("Content-Disposition", f"attachment;filename={self.get_filename()}")
        response.setHeader("Content-Type", f"application/pdf")
        return pdf_file.read()

    def get_data(self):
        """
        Should be implemented in your view.

        Returns:
            list of objects:

            Example:
                [
                    ["Mario", "22"],
                    ["Giovanna", "21"],
                ]
        """
        raise NotImplementedError()

    def format_row(self, item):
        """ """
        return item

    def get_columns(self, data):
        """
        Should be implemented in your view.

        Args:
            data: The input data used to determine headers
                  (type depends on implementation).

        Returns:
            list of dict: A list of header definitions, each represented as a dictionary with:
                - "title" (str): The display name of the column.
                - "key" (str): The corresponding field name in the data.
            Example:
                [
                    {"title": "Name", "key": "name"},
                    {"title": "Age", "key": "age"}
                ]
        """
        raise NotImplementedError()

    def get_html_for_pdf(self, data):
        """
        Generate HTML data from the provided data.
        """
        columns = self.get_columns(data)
        view = api.content.get_view(
            name="export_pdf",
            context=self,
            request=self.request,
        )

        return view(rows=data, columns=columns)

    def pdf_styles(self):
        return importlib.resources.read_text(
            "iosanita.contenttypes.browser.static", "export_pdf.css"
        )

    def pdf_title(self):
        context = self.context.context
        return context.Title()

    def pdf_description(self):
        return None

    def pdf_cell_format(self, column, value):
        if value is None:
            return {"type": "str", "value": value}
        if isinstance(value, dict):
            # e.g. {'token': 'in_corso', 'title': 'In corso'}
            return {"type": "str", "value": value.get("token")}
        # XXX: this is a guess
        if value.startswith("https://"):
            return {"type": "url", "url": value, "value": column["title"]}
        # XXX: this is a guess
        # 2025-05-21T00:00:00 -> isoformat date YYYY-MM-DD
        if re.match(r"^\d{4}-\d{2}-\d{2}T00:00:00$", value):
            return {"type": "str", "value": value.split("T")[0]}
        return {"type": "str", "value": str(value)}

    def pdf_logob64(self):
        """
        TODO
        """
        return None

    def pdf_last_update(self):
        # TODO: valutare localizzazione della data
        return datetime.now().strftime("%d/%m/%Y %H:%M")
