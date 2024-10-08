# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from plone.app.dexterity import textindexer
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IUlterioriInformazioni(model.Schema):
    ulteriori_informazioni = BlocksField(
        title=_("ulteriori_informazioni", default="Ulteriori informazioni"),
        description=_(
            "ulteriori_informazioni_help",
            default="Ulteriori informazioni non contemplate dai campi precedenti.",
        ),
        required=False,
    )

    model.fieldset(
        "ulteriori_informazioni",
        label=_("ulteriori_informazioni_label", default="Ulteriori informazioni"),
        fields=["ulteriori_informazioni"],
    )

    textindexer.searchable("ulteriori_informazioni")


@implementer(IUlterioriInformazioni)
@adapter(IDexterityContent)
class UlterioriInformazioni(object):
    """ """

    def __init__(self, context):
        self.context = context
