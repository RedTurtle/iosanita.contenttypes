# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from iosanita.contenttypes.interfaces import IoSanitaBackReferenceExtractor
from iosanita.contenttypes.interfaces.persona import IPersona
from iosanita.contenttypes.interfaces.servizio import IServizio
from iosanita.contenttypes.interfaces.struttura import IStruttura
from iosanita.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa
from plone.restapi.interfaces import ISerializeToJsonSummary
from zc.relation.interfaces import ICatalog
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission


LIMIT = 25


@implementer(IoSanitaBackReferenceExtractor)
@adapter(Interface, Interface)
class BackReferencesExtractor(object):

    reference_id = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """
        By default does not return anything
        """
        if not self.reference_id:
            return {}
        return self.get_back_references(reference_id=self.reference_id)

    def get_back_references(self, reference_id):
        """
        Return a mapping of back references splitted by portal_type.
        News Items are sorted by date, other are sorted by title
        """

        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        relations = catalog.findRelations(
            {
                "to_id": intids.getId(aq_inner(self.context)),
                "from_attribute": reference_id,
            }
        )
        data = {}
        for rel in relations:
            obj = intids.queryObject(rel.from_id)
            if obj is None:
                continue
            portal_type = obj.portal_type
            if checkPermission("zope2.View", obj):
                if portal_type not in data:
                    data[portal_type] = []
                summary = getMultiAdapter(
                    (obj, getRequest()), ISerializeToJsonSummary
                )()
                data[portal_type].append(summary)
        for portal_type, values in data.items():
            if portal_type == "News Item":
                data[portal_type] = sorted(
                    values, key=lambda k: k["Date"], reverse=True
                )[:LIMIT]
            else:
                data[portal_type] = sorted(values, key=lambda k: k["title"])[:LIMIT]
        return data


@implementer(IoSanitaBackReferenceExtractor)
@adapter(IServizio, Interface)
class BackReferencesExtractorServizio(BackReferencesExtractor):

    reference_id = "servizio_correlato"

    def __call__(self):
        """
        Servizio can also be referenced by a custom field
        """

        data = super().__call__()

        data.update(
            self.get_back_references(reference_id="servizio_procedura_riferimento")
        )
        return data


@implementer(IoSanitaBackReferenceExtractor)
@adapter(IStruttura, Interface)
class BackReferencesExtractorStruttura(BackReferencesExtractor):
    reference_id = "struttura_correlata"


@implementer(IoSanitaBackReferenceExtractor)
@adapter(IUnitaOrganizzativa, Interface)
class BackReferencesExtractorUnitaOrganizzativa(BackReferencesExtractor):
    reference_id = "uo_correlata"


@implementer(IoSanitaBackReferenceExtractor)
@adapter(IPersona, Interface)
class BackReferencesExtractorPersona(BackReferencesExtractor):
    reference_id = "persona_correlata"

    def __call__(self):
        data = super().__call__()

        # append additional references
        data.update(
            {
                "responsabile": self.get_back_references(
                    reference_id="responsabile_correlato"
                ),
                "personale": self.get_back_references(
                    reference_id="personale_correlato"
                ),
            }
        )
        return data
