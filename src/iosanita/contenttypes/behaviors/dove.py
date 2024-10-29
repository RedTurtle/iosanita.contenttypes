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

    provincia = schema.TextLine(
        title=_("provincia", default="Provincia"),
        description=_("help_provincia", default=""),
        required=True,
    )

    circoscrizione = schema.TextLine(
        title=_("circoscrizione", default="Circoscrizione"),
        description=_("help_circoscrizione", default=""),
        required=False,
    )

    # searchabletext indexer
    textindexer.searchable("street")
    textindexer.searchable("nome_sede")
    textindexer.searchable("provincia")
    textindexer.searchable("circoscrizione")
    textindexer.searchable("zip_code")
    textindexer.searchable("city")
    textindexer.searchable("country")

    model.fieldset(
        "dove",
        label=_("dove_label", default="Dove"),
        fields=[
            "nome_sede",
            "street",
            "zip_code",
            "city",
            "provincia",
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
