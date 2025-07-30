from io import FileIO
from Products.Five.browser import BrowserView
from zExceptions import NotFound
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
import csv
from io import StringIO
from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
# from reportlab.lib import colors
        

import os.path


class ISearchBlockTraverser(IPublishTraverse):
    pass

@implementer(ISearchBlockTraverser)
class SearchBlockTraverser(BrowserView):
    pass

@implementer(IPublishTraverse)
class SearchBlockDownload(BrowserView):
    def __init__(self, context, request):
        super().__init__(context, request)
        self.block_id = None
        self.format = "csv"

    def publishTraverse(self, request, name):
        """
        e.g.
        .../it/bandi/avvisi/searchblock/@@download/1ebe022a.csv?portal_type=...
        """
        if self.block_id is None:
            if "." in name:
                self.block_id, self.format = name.split(".", 2) 
            else:
                self.block_id = name
        else:
            raise NotFound("Not found")
        return self

    def __call__(self):
        """
        # 1. cercare il blocco in pagina (self.context.blocks)
        # 2. recuperare le colonne, i filtri base e l'ordinamento base
        # 3. sovrascrivere/aggiungere filtri e ordinamenti da querystring
        # 4. fare la ricerca
        # 5. fare export in csv/pdf a seconda del formato
        """
        # 1. Get the block from page
        import pdb; pdb.set_trace()
        context = self.context.context
        blocks = getattr(context, 'blocks', {})
        block_data = blocks.get(self.block_id)
        if not block_data:
            raise NotFound(f"Block {self.block_id} not found")

        if block_data['@type'] not in ['search']:
            raise NotFound(f"Block {self.block_id} not valid")

        # 2. Get columns, base filters and sorting
        columns = block_data.get('columns', [])
        query = block_data.get('query', {})
        sort_on = block_data.get('sort_on', '')
        sort_order = block_data.get('sort_order', 'ascending')

        # 3. Update/Add filters and sorting from query string
        for key, value in self.request.form.items():
            if key in ('sort_on', 'sort_order'):
                if key == 'sort_on':
                    sort_on = value
                else:
                    sort_order = value
            else:
                query[key] = value

        # 4. Execute the search
        catalog = self.context.portal_catalog
        results = catalog(**query)

        # 5. Export based on format
        if self.format.lower() == 'csv':
            return self.export_csv(results, columns)
        elif self.format.lower() == 'pdf':
            return self.export_pdf(results, columns)
        else:
            raise NotFound(f"Unsupported format: {self.format}")

    def export_csv(self, results, columns):
        """Export search results to CSV format."""
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(columns)
        
        # Write data rows
        for result in results:
            row = [getattr(result, col, '') for col in columns]
            writer.writerow(row)
        
        self.request.response.setHeader('Content-Type', 'text/csv')
        self.request.response.setHeader('Content-Disposition', 
                                      f'attachment; filename=export_{self.block_id}.csv')
        return output.getvalue()

    def export_pdf(self, results, columns):
        """Export search results to PDF format using WeasyPrint and a Page Template."""
        from weasyprint import HTML
        from weasyprint.text.fonts import FontConfiguration
        from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
        from datetime import datetime
        
        # Convert results to a list of dictionaries for the template
        result_data = []
        for result in results:
            result_dict = {}
            for col in columns:
                # Handle both dictionary-like and object-like access
                if hasattr(result, 'get'):
                    result_dict[col] = result.get(col, '')
                else:
                    result_dict[col] = getattr(result, col, '')
            result_data.append(result_dict)
        
        # Render the template with the data
        template = ViewPageTemplateFile('templates/export_pdf.pt')
        html_content = template(self, 
                              columns=columns,
                              results=result_data,
                              timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Generate PDF with WeasyPrint
        font_config = FontConfiguration()
        pdf_file = HTML(string=html_content, base_url=self.request.URL).write_pdf(font_config=font_config)
        
        # Set response headers
        self.request.response.setHeader('Content-Type', 'application/pdf')
        self.request.response.setHeader(
            'Content-Disposition',
            f'attachment; filename=export_{self.block_id}.pdf'
        )
        return pdf_file