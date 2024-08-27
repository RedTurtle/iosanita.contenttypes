# -*- coding: utf-8 -*-
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.component import queryMultiAdapter
from iosanita.contenttypes.interfaces import IoSanitaBackReferenceExtractor


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class BackReferences(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {
            "back-references": {
                "@id": f"{self.context.absolute_url()}/@back-references"
            }
        }
        if not expand:
            return result

        references = queryMultiAdapter(
            (self.context, self.request), IoSanitaBackReferenceExtractor
        )()
        result["back-references"].update(references)

        return result


class BackReferencesGet(Service):
    def reply(self):
        back_references = BackReferences(self.context, self.request)
        return back_references(expand=True)["back-references"]
