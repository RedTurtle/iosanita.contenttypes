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


@indexer(IDexterityContent)
def street(context):
    return getattr(context.aq_base, "street", None)


@indexer(IDexterityContent)
def zip_code(context):
    return getattr(context.aq_base, "zip_code", None)


@indexer(IDexterityContent)
def city(context):
    return getattr(context.aq_base, "city", None)


@indexer(IDexterityContent)
def provincia(context):
    return getattr(context.aq_base, "provincia", None)


@indexer(IDexterityContent)
def geolocation(context):
    return getattr(context.aq_base, "geolocation", None)


@indexer(IDexterityContent)
def has_geolocation(context):
    data = getattr(context.aq_base, "geolocation", None)
    if not data:
        return False
    if data.latitude == 0.0 and data.longitude == 0.0:
        return False
    return True
