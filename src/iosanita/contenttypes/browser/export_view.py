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


CONTENT_TYPES_MAPPING = {
    "csv": "text/comma-separated-values",
    "pdf": "application/pdf",
    "html": "text/html",
}


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
        self.set_headers()
        data = self.get_data()
        if not data:
            return ""
        resp_data = ""
        if self.export_type == "csv":
            resp_data = self.get_csv(data)
        elif self.export_type == "pdf":
            resp_data = self.get_pdf(data)
        elif self.export_type == "html":
            resp_data = self.get_html_for_pdf(data)
        return resp_data

    def get_filename(self):
        """
        Return the filename for the CSV export.
        """
        now = datetime.now().strftime("%Y_%m_%d_%H_%M")
        return f"export_{now}.{self.export_type}"

    def set_headers(self):
        """
        Set the headers for the response.
        """
        if self.export_type in ["pdf", "csv"]:
            self.request.response.setHeader(
                "Content-Disposition", f"attachment;filename={self.get_filename()}"
            )
        self.request.response.setHeader(
            "Content-Type", CONTENT_TYPES_MAPPING[self.export_type]
        )

    def get_csv(self, data):
        """
        Generate CSV data from the provided data.
        """
        columns = self.get_columns(data)

        csv_data = StringIO()
        csv_writer = csv.writer(csv_data, quoting=csv.QUOTE_ALL)
        csv_writer.writerow([c["title"] for c in columns])

        for item in data:
            csv_writer.writerow(self.format_row(item))
        return csv_data.getvalue().encode("utf-8")

    def get_pdf(self, data):
        html_str = self.get_html_for_pdf(data=data)
        pdf_file = BytesIO()
        HTML(string=html_str).write_pdf(pdf_file)
        pdf_file.seek(0)
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
        return importlib.resources.read_text("iosanita.contenttypes.browser", "static/export_pdf.css")

    def pdf_title(self):
        return None

    def pdf_description(self):
        return None

    def pdf_cell_format(self, column, value):
        if value is None:
            return {"type": "str", "value": value}
        # if not isinstance(value, str):
        #     import pdb; pdb.set_trace()
        # XXX: this is a guess
        if value.startswith("https://"):
            return {"type": "url", "url": value, "value": column["title"]}
        # 2025-05-21T00:00:00 -> isoformat date YYYY-MM-DD
        if re.match(r"^\d{4}-\d{2}-\d{2}T00:00:00$", value):
            value = value.split("T")[0]
        return {"type": "str", "value": str(value)}
