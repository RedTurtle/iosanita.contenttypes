# -*- coding: utf-8 -*-
from collective.address.behaviors import IAddress
from collective.geolocationbehavior.geolocation import IGeolocatable
from iosanita.contenttypes import _
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


class IDoveSchema(IGeolocatable, IAddress):
    nome_sede = schema.TextLine(
        title=_("nome_sede", default="Nome sede"),
        description=_(
            "help_nome_sede",
            default="Inserisci il nome della "
            "sede, se non è presente tra quelle del sito.",
        ),
        required=False,
    )

    quartiere = schema.TextLine(
        title=_("quartiere", default="Quartiere"),
        description=_("help_quartiere", default=""),
        required=False,
    )

    circoscrizione = schema.TextLine(
        title=_("circoscrizione", default="Circoscrizione"),
        description=_("help_circoscrizione", default=""),
        required=False,
    )

    # searchabletext indexer
    textindexer.searchable("nome_sede")
    textindexer.searchable("quartiere")
    textindexer.searchable("circoscrizione")


@provider(IFormFieldProvider)
class IDoveStruttura(IDoveSchema):
    model.fieldset(
        "dove",
        label=_("dove_label", default="Dove"),
        fields=[
            "nome_sede",
            "street",
            "zip_code",
            "city",
            "quartiere",
            "circoscrizione",
            "country",
            "geolocation",
        ],
    )


@provider(IFormFieldProvider)
class IDove(IDoveSchema):
    struttura_correlata = RelationList(
        title=_("struttura_correlata_label", default="Struttura di riferimento"),
        description=_(
            "struttura_correlata_help",
            default="Indicare una o più strutture che fanno a capo a questo contenuto.",
        ),
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        default=[],
        required=True,
    )
    form.widget(
        "struttura_correlata",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Struttura"]},
    )
    model.fieldset(
        "dove",
        label=_("dove_label", default="Dove"),
        description=_(
            "dove_help",
            default="Se la sede di questo contenuto non coincide con la Struttura di riferimento, compilare gli altri campi.",
        ),
        fields=[
            "struttura_correlata",
            "nome_sede",
            "street",
            "zip_code",
            "city",
            "quartiere",
            "circoscrizione",
            "country",
            "geolocation",
        ],
    )


@implementer(IDove)
@adapter(IDexterityContent)
class Dove(object):
    """ """

    def __init__(self, context):
        self.context = context


@implementer(IDoveStruttura)
@adapter(IDexterityContent)
class DoveStruttura(object):
    """ """

    def __init__(self, context):
        self.context = context
