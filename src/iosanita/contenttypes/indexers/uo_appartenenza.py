# -*- coding: utf-8 -*-
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.decorator import indexer


@indexer(IDexterityContent)
def uo_appartenenza_uid(context, **kw):
    return [
        x.to_object.UID()
        for x in getattr(context.aq_base, "uo_appartenenza", [])
        if x.to_object
    ]
