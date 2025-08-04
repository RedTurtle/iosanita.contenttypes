from .export_view import ExportViewDownload
from .export_view import ExportViewTraverser
from .export_view import IExportViewDownload
from .export_view import IExportViewTraverser
from copy import deepcopy
from iosanita.contenttypes import _
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.interfaces import ISerializeToJson
from zExceptions import BadRequest
from zExceptions import NotFound
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.interface import implementer

import logging


logger = logging.getLogger(__name__)


class ISearchBlockTraverser(IExportViewTraverser):
    pass


@implementer(ISearchBlockTraverser)
class SearchBlockTraverser(ExportViewTraverser):
    pass


@implementer(IExportViewDownload)
class SearchBlockDownload(ExportViewDownload):
    def __init__(self, context, request):
        super().__init__(context, request)
        self.block_id = None
        self.export_type = "csv"

    def publishTraverse(self, request, name):
        """
        e.g.
        .../it/bandi/avvisi/searchblock/@@download/1ebe022a.csv?portal_type=...
        """
        if self.block_id is None:
            if "." in name:
                self.block_id, self.export_type = name.split(".", 2)
            else:
                self.block_id = name
            # 1. Get the block from page
            context = self.context.context
            blocks = getattr(context, "blocks", {})
            block_data = deepcopy(blocks.get(self.block_id))
            if not block_data:
                raise NotFound(f"Block {self.block_id} not found")
            if block_data["@type"] not in ["search"]:
                raise NotFound(f"Block {self.block_id} not valid")
            self.block_data = block_data
        else:
            raise NotFound("Not found")
        return self

    def _query_from_searchtext(self):
        if self.request.form.get("search"):
            return [
                {
                    "i": "SearchableText",
                    "o": "plone.app.querystring.operation.string.contains",
                    "v": self.request.form["search"],
                }
            ]
        return []

    def _query_from_facets(self):
        query = []
        for facet in self.block_data.get("facets") or []:
            if facet["field"]["value"] in self.request.form:
                if self.request.form[facet["field"]["value"]] in ["null"]:
                    continue
                if facet["type"] == "daterangeFacet":
                    query.append(
                        {
                            "i": facet["field"]["value"],
                            "o": "plone.app.querystring.operation.date.between",
                            "v": self.request.form[facet["field"]["value"]].split(","),
                        }
                    )
                # {'@id': 'e1ba4f25-09a7-4329-9d12-05e6e8a354f7', 'field': {'label': 'Stato del bando', 'value': 'bando_state'}, 'hidden': False, 'multiple': False, 'type': 'checkboxFacet'}
                elif facet["type"] == "checkboxFacet" and not facet["multiple"]:
                    query.append(
                        {
                            "i": facet["field"]["value"],
                            "o": "plone.app.querystring.operation.selection.is",
                            "v": self.request.form[facet["field"]["value"]],
                        }
                    )
                else:
                    logger.warning("DEBUG: filter %s not implemnted", facet)
            else:
                logger.info("DEBUG: skip %s", facet)
        return query

    def get_data(self):
        """
        # 1. cercare il blocco in pagina (self.context.blocks)
        # 2. recuperare le colonne, i filtri base e l'ordinamento base
        # 3. sovrascrivere/aggiungere filtri e ordinamenti da querystring
        # 4. fare la ricerca
        # 5. fare export in csv/pdf a seconda del formato
        """
        # TODO: chi/cosa scrive sul db ? questa è da togliere a regime
        alsoProvides(self.request, IDisableCSRFProtection)

        # 2. Get columns, base filters and sorting
        columns = self.block_data.get("columns", [])

        query_data = self.block_data["query"]
        query = query_data["query"]
        sort_on = query_data.get("sort_on")
        sort_order = query_data.get("sort_order")

        import logging

        logging.info("DEBUG %s", self.request.form)

        # 3. Update/Add filters and sorting from query string
        for key, value in self.request.form.items():
            if key == "sort_on":
                sort_on = value
            elif key == "sort_order":
                sort_order = value
            # else:
            #     import pdb; pdb.set_trace()
            #     query[key] = value
        query += self._query_from_facets()
        query += self._query_from_searchtext()

        logging.info("DEBUG %s", query)

        querybuilder_parameters = dict(
            query=query,
            brains=True,
            # b_start=b_start,
            # b_size=b_size,
            # sort_on=sort_on,
            # sort_order=sort_order,
            # limit=limit,
        )
        if sort_on:
            querybuilder_parameters["sort_on"] = sort_on
        if sort_order:
            querybuilder_parameters["sort_order"] = sort_order

        context = self.context.context

        querybuilder = getMultiAdapter(
            (context, self.request), name="querybuilderresults"
        )

        # 4. Execute the search
        # catalog = self.context.portal_catalog
        # results = catalog(**query)
        try:
            results = querybuilder(**querybuilder_parameters)
        except KeyError:
            # This can happen if the query has an invalid operation,
            # but plone.app.querystring doesn't raise an exception
            # with specific info.
            raise BadRequest("Invalid query.")

        # XXX: potrebbe essere overkilling serializzare, forse basta la ricerca al
        #      catalogo
        fullobjects = True
        results = getMultiAdapter((results, self.request), ISerializeToJson)(
            fullobjects=fullobjects
        )

        for obj in results["items"]:
            yield [obj["title"]] + [obj.get(c["field"]) for c in columns]

    def get_columns(self, data):
        # Il titolo va aggiunto di default come prima colonna ?
        # anche la url ?
        columns = self.block_data.get("columns", [])
        return [{"key": "title", "title": _("Titolo")}] + [
            {"key": c["field"], "title": c["title"]} for c in columns
        ]
