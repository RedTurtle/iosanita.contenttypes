# -*- coding: utf-8 -*-
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from redturtle.bandi.interfaces import IBando
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJson)
@adapter(IBando, Interface)
class BandoSerializeToJson(SerializeFolderToJson):
    def get_approfondimenti(self, bando_view):
        """ """
        folders = bando_view.retrieveFolderDeepening()
        results = []

        for folder in folders:
            contents = bando_view.retrieveContentsOfFolderDeepening(folder["path"])
            if not contents:
                continue
            # fix results for enhancedlinks
            for content in contents:
                content["getObjSize"] = content.get("filesize", "")
                content["mime_type"] = content.get("content-type", "")
                content["enhanced_links_enabled"] = "filesize" in content
            folder.update({"children": contents})
            results.append(folder)
        return results

    def __call__(self, version=None, include_items=True):
        result = super().__call__(version=version, include_items=include_items)
        bando_view = self.context.restrictedTraverse("bando_view")
        result["approfondimenti"] = self.get_approfondimenti(bando_view)
        result["stato_bando"] = bando_view.getBandoState()
        return result
