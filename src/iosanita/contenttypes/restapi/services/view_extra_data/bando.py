# -*- coding: utf-8 -*-
from iosanita.contenttypes.interfaces import IoSanitaViewExtraData
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from redturtle.bandi.interfaces.bando import IBando
from plone.restapi.interfaces import ISerializeToJsonSummary
from zope.component import getMultiAdapter
from plone import api
from plone.restapi.serializer.utils import uid_to_url


@implementer(IExpandableElement)
@adapter(IBando, Interface)
class ApprofondimentiBando(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {
            "approfondimenti-bando": {
                "@id": f"{self.context.absolute_url()}/@approfondimenti-bando"
            }
        }
        if not expand:
            return result

        result["approfondimenti-bando"]["items"] = self.get_approfondimenti()

        return result

    def get_approfondimenti(self):
        """ """
        folders = self.context.listFolderContents(
            contentFilter={"portal_type": "Bando Folder Deepening"}
        )

        siteid = api.portal.get().getId()
        result = []

        for folder in folders:
            if folder.exclude_from_nav:
                continue
            folder_data = getMultiAdapter(
                (folder, self.request), ISerializeToJsonSummary
            )()
            folder_data["items"] = []
            for child in folder.listFolderContents():
                if child.exclude_from_nav:
                    continue
                child_data = getMultiAdapter(
                    (child, self.request), ISerializeToJsonSummary
                )()
                if child.portal_type == "Link":
                    url = getattr(child, "remoteUrl", "") or ""

                    if url.startswith("${portal_url}/resolveuid/"):
                        uid = url.replace("${portal_url}/", "")
                        child_data["@id"] = uid_to_url(uid)
                folder_data["items"].append(child_data)
            result.append(folder_data)
        return result


class ApprofondimentiBandoGet(Service):
    def reply(self):
        approfondimenti = ApprofondimentiBando(self.context, self.request)
        return approfondimenti(expand=True)["approfondimenti-bando"]
