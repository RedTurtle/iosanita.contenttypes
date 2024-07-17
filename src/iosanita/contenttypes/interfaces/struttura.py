# -*- coding: utf-8 -*-

from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces import IIosanitaContenttypes

from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from collective.volto.blocksfield.field import BlocksField
from plone.app.dexterity import textindexer


class IStruttura(model.Schema, IIosanitaContenttypes):
    """Marker interface for content type"""

    sottotitolo = schema.TextLine(
        title=_("sottotitolo_label", default="Sottotitolo"),
        description=_(
            "sottotitolo_help",
            default="Indica un eventuale sottotitolo/titolo alternativo.",
        ),
        required=False,
    )

    descrizione_estesa = BlocksField(
        title=_("descrizione_estesa_struttura_label", default="Descrizione estesa"),
        required=False,
        description=_(
            "descrizione_estesa_label_help",
            default="Descrizione più estesa della struttura con riferimento alle principali attività sanitarie svolte.",
        ),
    )

    come_accedere = BlocksField(
        title=_("come_accedere_label", default="Come accedere"),
        required=True,
        description=_(
            "come_accedere_help",
            default="Modalità di accesso alla struttura con particolare attenzione agli accessi per disabili ed eventuale descrizione di come arrivare, costi e regole di accesso.",
        ),
    )

    orari_apertura = BlocksField(
        title=_("orari_apertura_label", default="Orari di apertura"),
        required=True,
        description=_(
            "orari_apertura_help",
            default="Orario di apertura della struttura al pubblico.",
        ),
    )
    servizi = RelationList(
        title=_("servizi_label", default="Servizi"),
        default=[],
        value_type=RelationChoice(
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        missing_value=(),
        description=_(
            "servizi_help",
            default="Elenco dei servizi e delle prestazioni offerti dalla struttura.",
        ),
    )

    responsabile_struttura = RelationList(
        title=_(
            "responsabile_struttura_label",
            default="Responsabile struttura",
        ),
        description=_(
            "responsabile_struttura_help",
            default="La persona che dirige la struttura.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )

    coordinatore_struttura = RelationList(
        title=_(
            "coordinatore_struttura_label",
            default="Coordinatore della struttura",
        ),
        description=_(
            "responsabile_struttura_help",
            default="La persona che coordina la struttura.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )
    personale_struttura = RelationList(
        title=_(
            "personale_struttura_label",
            default="Personale della struttura",
        ),
        description=_(
            "personale_struttura_help",
            default="Elenco del personale che opera nella struttura.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )
    unita_organizzativa_appartenenza = RelationList(
        title=_(
            "unita_organizzativa_appartenenza_label",
            default="Unità organizzativa di appartenenza",
        ),
        description=_(
            "unita_organizzativa_appartenenza_help",
            default="",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )

    form.widget(
        "responsabile_struttura",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Persona"]},
    )
    form.widget(
        "coordinatore_struttura",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Persona"]},
    )
    form.widget(
        "personale_struttura",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Persona"]},
    )

    form.widget(
        "unita_organizzativa_appartenenza",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["UnitaOrganizzativa"]},
    )

    model.fieldset(
        "cosa_e",
        label=_("cosa_e_fieldset", default="Cos'è"),
        fields=["descrizione_estesa"],
    )

    model.fieldset(
        "come_accedere",
        label=_("come_accedere_label", default="Come accedere"),
        fields=["come_accedere"],
    )
    model.fieldset(
        "orari_apertura",
        label=_("orari_apertura_label", default="Orari di apertura"),
        fields=["orari_apertura"],
    )
    model.fieldset(
        "servizi",
        label=_("servizi_label", default="Servizi"),
        fields=["servizi"],
    )
    model.fieldset(
        "persone_struttura",
        label=_("persone_struttura_label", default="Persone struttura"),
        fields=[
            "responsabile_struttura",
            "coordinatore_struttura",
            "personale_struttura",
        ],
    )
    model.fieldset(
        "contenuti_collegati",
        label=_("contenuti_collegati_label", default="Contenuti collegati"),
        fields=["unita_organizzativa_appartenenza"],
    )

    # SearchableText
    textindexer.searchable("sottotitolo")
