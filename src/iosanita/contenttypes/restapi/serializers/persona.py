# -*- coding: utf-8 -*-
#from .related_news_serializer import SerializeFolderToJson
from Acquisition import aq_inner
from iosanita.contenttypes.interfaces.persona import IPersona
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.dxcontent import SerializeToJson

from zc.relation.interfaces import ICatalog
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission


@implementer(ISerializeToJson)
@adapter(IPersona, Interface)
class PersonaSerializer(SerializeToJson):
    index = "news_people"

    def related_contents(self, field):
        """ """
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        items = []
        relations = catalog.findRelations(
            dict(
                to_id=intids.getId(aq_inner(self.context)),
                from_attribute=field,
            )
        )

        for rel in relations:
            obj = intids.queryObject(rel.from_id)
            if obj is not None and checkPermission("zope2.View", obj):
                summary = getMultiAdapter(
                    (obj, getRequest()), ISerializeToJsonSummary
                )()
                items.append(summary)
        return sorted(items, key=lambda k: k["title"])


    def get_structure_backreferences(self, ct_type):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        obj_intid = intids.getId(self.context)
        relations = catalog.findRelations({"to_id": obj_intid})
        backreferences = [relation.from_object for relation in relations]

        return [
            getMultiAdapter((i, self.request), ISerializeToJsonSummary)
            for i in backreferences
            if i.portal_type == ct_type
        ]
    
    def __call__(self, version=None, include_items=True):
        result = super(PersonaSerializer, self).__call__(
            version=version, include_items=include_items
        )
        
        if getattr(self.context, "incarichi", ""):
            result["ruolo"] = getattr(self.context, "incarichi").raw
            
        result["organizzazione_riferimento"] = self.get_service_backreferences("UnitaOrganizzativa")
        result["strutture_in_cui_opera"] = self.get_service_backreferences("Struttura")

        return result
