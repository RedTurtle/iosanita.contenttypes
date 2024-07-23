# -*- coding: utf-8 -*-
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.decorator import indexer


@indexer(IDexterityContent)
def parent(context):
    obj_parent = context.aq_parent
    return {
        "title": obj_parent.Title(),
        "UID": obj_parent.UID(),
        "@id": obj_parent.absolute_url(),
        "@type": obj_parent.portal_type,
    }


@indexer(IDexterityContent)
def exclude_from_search(context):
    return getattr(context.aq_base, "exclude_from_search", False)
