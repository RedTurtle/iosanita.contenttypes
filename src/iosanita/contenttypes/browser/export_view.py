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
import six


CONTENT_TYPES_MAPPING = {
    "csv": '"text/comma-separated-values"',
    "pdf": '"application/pdf"',
}


class IExportViewTraverser(IPublishTraverse):
    """
    Marker interface for Download views
    """


@implementer(IExportViewTraverser)
class ExportViewTraverser(BrowserView):
    pass


@implementer(IPublishTraverse)
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
        if self.export_type not in ["csv", "pdf"]:
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
        headers = self.get_headers(data)

        csv_data = StringIO()
        csv_writer = csv.writer(csv_data, quoting=csv.QUOTE_ALL)
        csv_writer.writerow(headers)

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
        Implement it into your view
        """
        raise NotImplementedError()

    def get_headers(self, data):
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

    def get_table_data(self, data):
        """
        Implement it into your view
        """
        raise NotImplementedError()

    def format_row(self, item):
        """ """
        return item

    def get_html_for_pdf(self, data):
        """
        Generate HTML data from the provided data.
        """
        raise NotImplementedError()

        # example
        # view = api.content.get_view(
        #     name=self.pdf_template, context=self.context, request=self.request
        # )
        # return view(data=data)
