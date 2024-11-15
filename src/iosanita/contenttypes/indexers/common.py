# -*- coding: utf-8 -*-
from iosanita.contenttypes.interfaces.persona import IPersona
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.decorator import indexer

import re


def get_geolocation_data(context):
    geolocation = getattr(context.aq_base, "geolocation", None)
    if not geolocation:
        return {}

    title = getattr(context.aq_base, "nome_sede", "") or context.title
    street = getattr(context.aq_base, "street", "")
    city = getattr(context.aq_base, "city", "")
    provincia = getattr(context.aq_base, "provincia", "")

    address = ""

    if street:
        address += f"{street}"
    if city:
        address += f" {city}"
    if provincia:
        address += f" ({provincia})"

    return {
        "latitude": geolocation.latitude,
        "longitude": geolocation.longitude,
        "title": title,
        "address": re.sub(r"\s+", " ", address),
    }


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
    data = get_geolocation_data(context)
    if data:
        return [data]
    return []


@indexer(IPersona)
def geolocation_persona(context):
    """
    Persona can have multiple locations
    """
    res = []
    local_data = get_geolocation_data(context)
    if local_data:
        res.append(local_data)

    for field in ["struttura_in_cui_opera", "struttura_ricevimento"]:
        value = getattr(context.aq_base, field, [])
        if not value:
            continue
        for ref in value:
            ref_obj = ref.to_object
            if ref_obj:
                data = get_geolocation_data(ref_obj)
                if data:
                    res.append(data)
    return res


@indexer(IDexterityContent)
def has_geolocation(context):
    data = getattr(context.aq_base, "geolocation", None)
    if not data:
        return False
    if data.latitude == 0.0 and data.longitude == 0.0:
        return False
    return True


@indexer(IPersona)
def has_geolocation_persona(context):
    """
    Persona can have several locations
    """
    struttura_in_cui_opera = getattr(context.aq_base, "struttura_in_cui_opera", [])
    struttura_ricevimento = getattr(context.aq_base, "struttura_ricevimento", [])
    if struttura_in_cui_opera or struttura_ricevimento:
        return True
    data = getattr(context.aq_base, "geolocation", None)
    if not data:
        return False
    if data.latitude == 0.0 and data.longitude == 0.0:
        return False
    return True
