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


# TODO: migration script for these commented fields towards PDC
# contact_info
# Probabilmente non possibile trattandosi di un campo a blocchi
# preferirei si arrangiassero le redazioni. Altrimenti si defaulta
# ad un tipo a caso + tutto il testo e poi si arrangiano comunque
class IUnitaOrganizzativa(model.Schema):
    """Marker interface for content type UnitaOrganizzativa"""

    subtitle = schema.TextLine(
        title=_(
            "subtitle_label",
            default="Subtitle",
        ),
        required=False,
    )

    competenze = BlocksField(
        title=_("uo_competenze_label", default="Competenze"),
        description=_(
            "uo_competenze_help",
            default="Descrizione dei compiti assegnati alla struttura.",
        ),
        required=True,
    )

    responsabile = RelationList(
        title=_("responsabile_label", default="Responsabile"),
        value_type=RelationChoice(
            title=_("Responsabile"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "responsabile_help",
            default="Selezionare il/i responsabile/i della struttura.",
        ),
        default=[],
        required=False,
    )

    # vocabolario di riferimento sara' dinamico con i content type persona
    persone_struttura = RelationList(
        title=_(
            "persone_struttura_label", default="Persone che compongono la struttura"
        ),
        default=[],
        value_type=RelationChoice(
            title=_("Persone della struttura"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "persone_struttura_help",
            default="Seleziona la lista delle persone che compongono" " la struttura.",
        ),
        required=False,
    )

    documenti_pubblici = RelationList(
        title=_("documenti_pubblici_label", default="Documenti pubblici"),
        default=[],
        description=_(
            "documenti_pubblici_help",
            default="Documenti pubblici importanti, collegati a questa Unità Organizzativa",  # noqa
        ),
        value_type=RelationChoice(
            title=_("Documenti pubblici"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    #  custom widgets
    form.widget(
        "documenti_pubblici",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["Documento"],
        },
    )
    form.widget(
        "persone_struttura",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Persona"]},
    )
    form.widget(
        "responsabile",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Persona"],
            # "basePath": "/amministrazione",
        },
    )

    # custom fieldsets and order
    model.fieldset(
        "cosa_fa",
        label=_("cosa_fa_label", default="Competenze"),
        fields=["competenze"],
    )
    model.fieldset(
        "struttura",
        label=_("unita_organizzativa_struttura_label", default="Struttura"),
        fields=[
            "responsabile",
        ],
    )
    model.fieldset(
        "persone",
        label=_("persone_label", default="Persone"),
        fields=["persone_struttura"],
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=[],
    )

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["documenti_pubblici"],
    )

    form.order_after(documenti_pubblici="relatedItems")

    # SearchableText indexers
    textindexer.searchable("competenze")
    textindexer.searchable("responsabile")
