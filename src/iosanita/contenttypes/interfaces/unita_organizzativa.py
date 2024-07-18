# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IUnitaOrganizzativa(model.Schema):
    """Marker interface for content type UnitaOrganizzativa"""

    competenze = BlocksField(
        title=_("uo_competenze_label", default="Competenze"),
        description=_(
            "uo_competenze_help",
            default="Descrizione dei compiti assegnati alla struttura.",
        ),
        required=True,
    )

    responsabile_uo = RelationList(
        title=_("responsabile_label", default="Responsabile"),
        description=_(
            "responsabile_uo_help",
            default="La persona che dirige l'unità organizzativa.",
        ),
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        default=[],
        required=True,
    )

    personale_uo = RelationList(
        title=_("personale_label", default="Personale"),
        description=_(
            "personale_uo_help",
            default="Elenco del personale che opera nell'unità organizzativa.",
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
    )

    struttura_correlata = RelationChoice(
        title=_("struttura_correlata_label", default="Struttura correlata"),
        description=_(
            "struttura_correlata_uo_help",
            default="Seleziona la sede di questa unità organizzativa. "
            "Se la sede è una Struttura, utilizza questo campo. "
            "In alternativa compila i campi successivi.",
        ),
        vocabulary="plone.app.vocabularies.Catalog",
        required=False,
    )

    orari_apertura = BlocksField(
        title=_("orari_apertura_label", default="Orari di apertura"),
        description=_(
            "orari_apertura_help",
            default="Indicazione delle fasce orarie in cui è possibile contattare o accedere all'unità organizzativa.",
        ),
        required=True,
    )

    documenti = RelationList(
        title=_("documenti_label", default="Documenti"),
        default=[],
        description=_(
            "documenti_help",
            default="Seleziona dei documenti correlati.",
        ),
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
    )

    #  custom widgets
    form.widget(
        "documenti",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["Documento"],
        },
    )
    form.widget(
        "personale_uo",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Persona"]},
    )
    form.widget(
        "responsabile_uo",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Persona"],
            # "basePath": "/amministrazione",
        },
    )
    form.widget(
        "struttura_correlata",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["Struttura"],
        },
    )

    # custom fieldsets and order
    model.fieldset(
        "cosa_fa",
        label=_("cosa_fa_label", default="Competenze"),
        fields=["competenze"],
    )
    model.fieldset(
        "persone_uo",
        label=_("persone_uo_fieldset_label", default="Persone Unità organizzativa"),
        fields=[
            "responsabile_uo",
            "personale_uo",
        ],
    )
    model.fieldset(
        "dove",
        label=_("dove_label", default="Dove"),
        description=_(
            "dove_uo_label",
            default="Se la sede dell'Unità organizzativa è una Struttura presente nel sito, utilizza il relativo campo per correlarla. "
            "In alternativa puoi selezionare un Luogo, o come ultima opzione inserire i dati a mano.",
        ),
        fields=["struttura_correlata"],
    )
    model.fieldset(
        "orari_apertura",
        label=_("orari_apertura_label", default="Orari di apertura"),
        fields=["orari_apertura"],
    )

    model.fieldset(
        "documenti",
        label=_("documenti_label", default="Documenti"),
        fields=["documenti"],
    )

    # SearchableText indexers
    textindexer.searchable("competenze")
    textindexer.searchable("orari_apertura")
