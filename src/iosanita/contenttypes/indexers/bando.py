# -*- coding: utf-8 -*-
from redturtle.bandi.interfaces import IBando
from plone.indexer.decorator import indexer


@indexer(IBando)
def Subject_bando(context, **kw):
    return context.Subject
