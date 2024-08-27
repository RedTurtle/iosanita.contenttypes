# -*- coding: utf-8 -*-
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from iosanita.contenttypes.interfaces.servizio import IServizio
from iosanita.contenttypes.interfaces.struttura import IStruttura
from iosanita.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa
from iosanita.contenttypes.interfaces.persona import IPersona
from plone import api
from plone.restapi.interfaces import ISerializeToJsonSummary
from zope.component import queryMultiAdapter
from iosanita.contenttypes.interfaces import IoSanitaBackReferenceExtractor
from zc.relation.interfaces import ICatalog
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from Acquisition import aq_inner


@implementer(IoSanitaBackReferenceExtractor)
@adapter(Interface, Interface)
class BackReferencesExtractor(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """
        By default does not return anything
        """
        return {}

    def get_related_news(self, reference_field):
        """
        We use portal_catalog to return back references because we want news in
        order of effective date
        """
        query = {
            "portal_type": "News Item",
            reference_field: self.context.UID(),
            "sort_on": "Date",
            "sort_order": "reverse",
        }
        brains = api.content.find(**query)[:15]

        return [
            queryMultiAdapter((brain, self.request), ISerializeToJsonSummary)()
            for brain in brains
        ]

    def get_back_reference(self, reference_id):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        relations = catalog.findRelations(
            dict(
                to_id=intids.getId(aq_inner(self.context)),
                from_attribute=reference_id,
            )
        )
        data = []
        for rel in relations:
            obj = intids.queryObject(rel.from_id)
            if obj is not None and checkPermission("zope2.View", obj):
                summary = getMultiAdapter(
                    (obj, getRequest()), ISerializeToJsonSummary
                )()
                data.append(summary)
        return sorted(data, key=lambda k: k["title"])


@implementer(IoSanitaBackReferenceExtractor)
@adapter(IServizio, Interface)
class BackReferencesExtractorServizio(BackReferencesExtractor):
    def __call__(self):
        return {
            "news": self.get_related_news(reference_field="servizio_correlato"),
            "documenti": self.get_back_reference(
                reference_id="servizio_procedura_riferimento"
            ),
        }


@implementer(IoSanitaBackReferenceExtractor)
@adapter(IStruttura, Interface)
class BackReferencesExtractorStruttura(BackReferencesExtractor):
    def __call__(self):
        return {
            "news": self.get_related_news(reference_field="struttura_correlata"),
        }


@implementer(IoSanitaBackReferenceExtractor)
@adapter(IUnitaOrganizzativa, Interface)
class BackReferencesExtractorUnitaOrganizzativa(BackReferencesExtractor):
    def __call__(self):
        return {
            "news": self.get_related_news(reference_field="uo_correlata"),
        }


@implementer(IoSanitaBackReferenceExtractor)
@adapter(IPersona, Interface)
class BackReferencesExtractorPersona(BackReferencesExtractor):
    def __call__(self):
        return {
            "responsabile": self.get_back_reference(
                reference_id="responsabile_correlato"
            ),
            "personale": self.get_back_reference(reference_id="personale_correlato"),
        }
