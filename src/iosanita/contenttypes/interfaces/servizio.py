# -*- coding: utf-8 -*-

from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces import IIosanitaContenttypes
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IServizio(model.Schema, IIosanitaContenttypes):
    """Marker interface for content type"""

    stato_servizio = schema.Bool(
        title=_("stato_servizio_label", default="Stato servzio"),
        required=False,
        description=_(
            "stato_servizio_help",
            default="Indica se il servizio è effettivamente fruibile o meno. "
            "Spuntare se non è fruibile.",
        ),
    )

    cosa_serve = BlocksField(
        title=_("cosa_serve_label", default="Cosa serve"),
        required=True,
        description=_(
            "cosa_serve_help",
            default="Descrizione delle istruzioni per usufruire del servizio.",
        ),
    )

    come_accedere = BlocksField(
        title=_("come_accedere_label", default="Come accedere"),
        required=True,
        description=_(
            "come_accedere_help",
            default="Descrizione della procedura da seguire per poter"
            " usufruire del servizio.",
        ),
    )
    orari = BlocksField(
        title=_("orari_servizio_label", default="Orari del servizio"),
        required=True,
        description=_(
            "orari_servizio_help",
            default="Indicazione dell'orario in cui è possibile usufruire del servizio o della prestazione. "
            "Se gli orari del servizio coincidono con quelli della struttura che lo eroga, ripeterli anche qui.",
        ),
    )

    piattaforma_online_link = schema.TextLine(
        title=_("piattaforma_online_link_label", default="Piattaforma online"),
        description=_(
            "piattaforma_online_link_help",
            default="Collegamento con l'eventuale piattaforma online del servzio.",
        ),
        required=False,
    )
    piattaforma_online_label = schema.TextLine(
        title=_(
            "piattaforma_online_label",
            default="Etichetta bottone per piattaforma online",
        ),
        description=_(
            "piattaforma_online_help",
            default="Testo da mostrare nel bottone del link alla piattaforma online.",
        ),
        default="Prenota online",
        required=False,
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

    tempi_attesa = BlocksField(
        title=_("tempi_attesa_label", default="Tempi di attesa"),
        required=True,
        description=_("tempi_attesa_help", default=""),
    )
    costi = BlocksField(
        title=_("costi_label", default="Costi"),
        required=True,
        description=_("costi_help", default=""),
    )

    descrizione_estesa = BlocksField(
        title=_("descrizione_estesa_label", default="Descrizione estesa"),
        required=False,
        description=_(
            "descrizione_estesa_servizio_help",
            default="Descrizione estesa e completa del servizio o della prestazione. "
            "Se si sta descrivendo un Percorso di Cura specificare contestualmente l'elenco delle prestazioni afferenti al percorso.",
        ),
    )
    procedure_collegate_esito = BlocksField(
        title=_(
            "procedure_collegate_esito_label", default="Procedure collegate all'esito"
        ),
        description=_(
            "procedure_collegate_esito_help",
            default="Spiegazione relativa all'esito della procedura e dove eventualmente "
            "sarà disponibile o sarà possibile ritirare l'esito (sede dell'ufficio, orari, numero sportello, etc.)",
        ),
        required=False,
    )

    uo_correlata = RelationList(
        title=_(
            "uo_correlata_servizio_label", default="Unità organizzativa responsabile"
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=True,
        missing_value=(),
    )
    responsabile_correlato = RelationList(
        title=_(
            "responsabile_correlato_servizio_label", default="Responsabile del servizio"
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=True,
        missing_value=(),
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
        "uo_correlata",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )
    form.widget(
        "responsabile_correlato",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["Persona"],
        },
    )

    # fieldsets
    model.fieldset(
        "cosa_serve",
        label=_("cosa_serve_label", default="Cosa serve"),
        fields=["cosa_serve"],
    )
    model.fieldset(
        "accedi_al_servizio",
        label=_("accedi_al_servizio_label", default="Accedi al servizio"),
        fields=["come_accedere", "piattaforma_online_link", "piattaforma_online_label"],
    )
    model.fieldset(
        "tempi_attesa",
        label=_("tempi_attesa_label", default="Tempi di attesa"),
        fields=["tempi_attesa"],
    )
    model.fieldset(
        "costi",
        label=_("costi_label", default="Costi"),
        fields=["costi"],
    )
    model.fieldset(
        "dove",
        label=_("dove_label", default="Dove"),
        fields=["struttura_correlata"],
    )
    model.fieldset(
        "orari",
        label=_("orari_servizio_label", default="Orari del servizio"),
        fields=["orari"],
    )
    model.fieldset(
        "cosa_e",
        label=_("cosa_e_fieldset", default="Cos'è"),
        fields=["descrizione_estesa"],
    )
    model.fieldset(
        "procedure_collegate_esito",
        label=_(
            "procedure_collegate_esito_label", default="Procedure collegate all'esito"
        ),
        fields=["procedure_collegate_esito"],
    )
    model.fieldset(
        "responsabili",
        label=_("responsabili_label", default="Responsabili"),
        fields=["uo_correlata", "responsabile_correlato"],
    )

    textindexer.searchable("cosa_serve")
