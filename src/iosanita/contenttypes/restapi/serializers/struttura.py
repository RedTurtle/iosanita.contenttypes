# -*- coding: utf-8 -*-
from plone.restapi.serializer.dxcontent import SerializeToJson as BaseSerializer
from Acquisition import aq_inner
from iosanita.contenttypes.interfaces.struttura import IStruttura
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


@implementer(ISerializeToJson)
@adapter(IStruttura, Interface)
class StrutturaSerializer(BaseSerializer):
    def get_people(self):
        """ """
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        people = []
        objs_unique = [] 
        for attr in ["struttura_ricevimento", "struttura_in_cui_opera"]:
            relations = catalog.findRelations(
                dict(
                    to_id=intids.getId(aq_inner(self.context)),
                    from_attribute=attr,
                )
            )

            for rel in relations:
                obj = intids.queryObject(rel.from_id)
                if (
                    obj is not None
                    and obj.UID() not in objs_unique
                    and checkPermission("zope2.View", obj)  # noqa
                    and obj.portal_type == "Persona"  # noqa
                ):
                    summary = getMultiAdapter(
                        (obj, getRequest()), ISerializeToJsonSummary
                    )()
                    people.append(summary)
                    objs_unique.append(obj.UID())

        
        return sorted(people, key=lambda k: k["title"])

    def __call__(self, version=None, include_items=True):
        result = super(StrutturaSerializer, self).__call__(
            version=version, include_items=include_items
        )

        result["personale_struttura"] = json_compatible(self.get_people())

        return result
