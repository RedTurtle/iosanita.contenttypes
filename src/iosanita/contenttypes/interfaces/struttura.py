# -*- coding: utf-8 -*-

from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces import IIosanitaContenttypes
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList


class IStruttura(model.Schema, IIosanitaContenttypes):
    """Marker interface for content type"""

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

    responsabile_struttura = RelationList(
        title=_(
            "responsabile_struttura_label",
            default="Responsabile",
        ),
        description=_(
            "responsabile_help",
            default="La persona che dirige la struttura.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )

    coordinatore_struttura = RelationList(
        title=_(
            "coordinatore_label",
            default="Coordinatore",
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
            "personale_label",
            default="Personale",
        ),
        description=_(
            "personale_struttura_help",
            default="Elenco del personale che opera nella struttura.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )
    uo_appartenenza = RelationList(
        title=_(
            "uo_appartenenza_label",
            default="Unità organizzativa di appartenenza",
        ),
        description=_(
            "uo_appartenenza_help",
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
        "uo_appartenenza",
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
        fields=["uo_appartenenza"],
    )
