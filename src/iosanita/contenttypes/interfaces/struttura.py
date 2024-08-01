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
        title=_("descrizione_estesa_label", default="Descrizione estesa"),
        required=False,
        description=_(
            "descrizione_estesa_struttura_help",
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

    orari = BlocksField(
        title=_("orari_struttura_label", default="Orari di apertura"),
        required=True,
        description=_(
            "orari_struttura_help",
            default="Orari di apertura della struttura al pubblico.",
        ),
    )

    responsabile_correlato = RelationList(
        title=_(
            "responsabile_correlato_struttura_label",
            default="Responsabile",
        ),
        description=_(
            "responsabile_correlato_struttura_help",
            default="La persona che dirige la struttura.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )

    coordinatore_correlato = RelationList(
        title=_(
            "coordinatore_correlato_struttura_label",
            default="Coordinatore",
        ),
        description=_(
            "coordinatore_correlato_struttura_help",
            default="La persona che coordina la struttura.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )
    uo_correlata = RelationList(
        title=_(
            "uo_correlata_struttura_label",
            default="Unità organizzativa di appartenenza",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )
    struttura_correlata = RelationList(
        title=_(
            "struttura_correlata_label",
            default="Struttura correlata",
        ),
        description=_(
            "struttura_correlata_help",
            default="Seleziona una struttura correlata.",
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
        missing_value=(),
    )

    servizi = RelationList(
        title=_("servizi_label", default="Servizi"),
        default=[],
        value_type=RelationChoice(
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=True,
        missing_value=(),
        description=_(
            "servizi_help",
            default="Elenco dei servizi e delle prestazioni offerti.",
        ),
    )

    # widgets
    form.widget(
        "struttura_correlata",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["Struttura"],
        },
    )
    form.widget(
        "responsabile_correlato",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Persona"]},
    )
    form.widget(
        "coordinatore_correlato",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Persona"]},
    )

    form.widget(
        "uo_correlata",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["UnitaOrganizzativa"]},
    )

    form.widget(
        "servizi",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Servizio"]},
    )

    # fieldsets
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
        "orari",
        label=_("orari_label", default="Orari di apertura"),
        fields=["orari"],
    )

    model.fieldset(
        "contenuti_collegati",
        label=_("contenuti_collegati_label", default="Contenuti collegati"),
        fields=["uo_correlata", "struttura_correlata"],
    )

    model.fieldset(
        "servizi",
        label=_("servizi_label", default="Servizi"),
        fields=["servizi"],
    )
