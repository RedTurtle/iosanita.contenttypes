# -*- coding: utf-8 -*-
from iosanita.contenttypes import _
from plone.app.dexterity import textindexer
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IParliamoDi(model.Schema):
    """Marker interface for Argomenti"""

    parliamo_di = schema.Choice(
        title=_("parliamo_di_label", default="Parliamo di"),
        description=_(
            "parliamo_di_help",
            default="Seleziona una lista di argomenti d'interesse per questo contenuto.",
        ),
        vocabulary="collective.taxonomy.tipologia_argomento",
        required=False,
        default="",
    )

    textindexer.searchable("parliamo_di")


@implementer(IParliamoDi)
@adapter(IDexterityContent)
class ParliamoDi(object):
    """"""

    def __init__(self, context):
        self.context = context
