# -*- coding: utf-8 -*-
from collective.address.behaviors import IAddress
from collective.geolocationbehavior.geolocation import IGeolocatable
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
class IDove(IGeolocatable, IAddress):
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


@implementer(IDove)
@adapter(IDexterityContent)
class Dove(object):
    """ """

    def __init__(self, context):
        self.context = context
