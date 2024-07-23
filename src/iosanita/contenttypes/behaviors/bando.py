# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IBando(model.Schema):
    """Marker interface for content type Bando"""

    descrizione_estesa = BlocksField(
        title=_("descrizione_estesa_label", default="Cos'è"),
        required=True,
        description=_(
            "descrizione_estesa_bando_help",
            default="Descrizione dettagliata e completa.",
        ),
    )

    come_partecipare = BlocksField(
        title=_("come_partecipare_label", default="Come partecipare"),
        required=True,
        description=_(
            "come_partecipare_help",
            default="Descrizione delle modalità di partecipazione al bando o al concorso e collegamento.",
        ),
    )
    modalita_selezione = BlocksField(
        title=_("modalita_selezione_label", default="Modalità di selezione"),
        required=True,
        description=_(
            "modalita_selezione_help",
            default="Informazioni sulle modalità di selezione, ad esempio da quante prove e di che tipo è composta la selezione.",
        ),
    )

    # custom widgets

    # custom fieldsets and order
    model.fieldset(
        "cosa_e",
        label=_("cosa_e_fieldset", default="Cos'è"),
        fields=[
            "descrizione_estesa",
        ],
    )
    model.fieldset(
        "come_partecipare",
        label=_("come_partecipare_label", default="Come partecipare"),
        fields=[
            "come_partecipare",
        ],
    )
    model.fieldset(
        "modalita_selezione",
        label=_("modalita_selezione_label", default="Modalità di selezione"),
        fields=[
            "modalita_selezione",
        ],
    )

    textindexer.searchable("descrizione_estesa")


@implementer(IBando)
@adapter(IDexterityContent)
class Bando(object):
    """ """

    def __init__(self, context):
        self.context = context
