# -*- coding: utf-8 -*-
from plone.app.dexterity import textindexer
from iosanita.contenttypes import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from zope import schema
from plone.autoform import directives as form


@provider(IFormFieldProvider)
class ISottotitolo(model.Schema):
    """Marker interface"""

    sottotitolo = schema.TextLine(
        title=_("sottotitolo_label", default="Sottotitolo"),
        description=_(
            "sottotitolo_help",
            default="Indica un eventuale sottotitolo/titolo alternativo.",
        ),
        required=False,
    )
    form.order_after(sottotitolo="IBasic.description")

    # SearchableText
    textindexer.searchable("sottotitolo")


@implementer(ISottotitolo)
@adapter(IDexterityContent)
class Sottotitolo(object):
    """"""

    def __init__(self, context):
        self.context = context
