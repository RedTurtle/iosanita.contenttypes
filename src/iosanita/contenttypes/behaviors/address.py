# -*- coding: utf-8 -*-
from collective.address.behaviors import IAddress
from iosanita.contenttypes import _
from plone.app.dexterity import textindexer
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form


class IAddressNomeSede(model.Schema):
    nome_sede = schema.TextLine(
        title=_("nome_sede", default="Nome sede"),
        description=_(
            "help_nome_sede",
            default="Inserisci il nome della "
            "sede, se non è presente tra quelle del sito.",
        ),
        required=False,
    )
    textindexer.searchable("nome_sede")


class IAddressLocal(model.Schema):
    """ """

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
    textindexer.searchable("quartiere")
    textindexer.searchable("circoscrizione")


@provider(IFormFieldProvider)
class IAddressVenue(IAddress, IAddressLocal):
    """"""

    model.fieldset(
        "dove",
        label=_("dove_label", default="Dove"),
        fields=[
            "street",
            "zip_code",
            "city",
            "quartiere",
            "circoscrizione",
            "country",
        ],
    )


@provider(IFormFieldProvider)
class IAddressEvent(IAddress, IAddressNomeSede, IAddressLocal):
    """"""

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
        ],
    )


@provider(IFormFieldProvider)
class IAddressPersona(IAddress, IAddressNomeSede, IAddressLocal):
    """"""

    model.fieldset(
        "dove",
        label=_("struttura_label", default="Dove"),
        fields=[
            "nome_sede",
            "street",
            "zip_code",
            "city",
            "quartiere",
            "circoscrizione",
            "country",
        ],
    )


@provider(IFormFieldProvider)
class IAddressUnitaOrganizzativa(IAddress, IAddressNomeSede, IAddressLocal):
    """"""

    structure =  RelationList(
        title=_("strutura_label", default="Structure"),
        value_type=RelationChoice(
            title=_("structure_relation_label"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        default=[],
    )
    form.widget(
        "structure",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Struttura"],
        },
    )
    model.fieldset(
        "dove",
        label=_("struttura_label", default="Dove"),
        fields=[
            "nome_sede",
            "street",
            "zip_code",
            "city",
            "quartiere",
            "circoscrizione",
            "country",
            "structure"
        ],
    )


@implementer(IAddressVenue)
@adapter(IDexterityContent)
class AddressVenue(object):
    """ """

    def __init__(self, context):
        self.context = context


@implementer(IAddressEvent)
@adapter(IDexterityContent)
class AddressEvent(object):
    """ """

    def __init__(self, context):
        self.context = context


@implementer(IAddressPersona)
@adapter(IDexterityContent)
class AddressPersona(object):
    """ """

    def __init__(self, context):
        self.context = context

@implementer(IAddressUnitaOrganizzativa)
@adapter(IDexterityContent)
class AddressUnitaOrganizzativa(object):
    """ """

    def __init__(self, context):
        self.context = context
