# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from zc.relation.interfaces import ICatalog
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from plone.restapi.serializer.dxcontent import SerializeToJson
from plone.memoize.view import memoize
from Products.Five import BrowserView
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.intid.interfaces import IIntIds


from iosanita.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa


@implementer(ISerializeToJson)
@adapter(IUnitaOrganizzativa, Interface)
class UOSerializer(SerializeToJson):
    def get_structure_backreferences(self):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        obj_intid = intids.getId(self.context)
        relations = catalog.findRelations({"to_id": obj_intid})
        backreferences = [relation.from_object for relation in relations]

        return [
            getMultiAdapter((i, self.request), ISerializeToJsonSummary)
            for i in backreferences
            if i.portal_type == "Struttura"
        ]

    def __call__(self, *args, **kwargs):
        result = super().__call__(*args, **kwargs)

        result["structure_backreferences"] = self.get_service_backreferences()

        return result
