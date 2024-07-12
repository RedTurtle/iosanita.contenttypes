# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
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


@provider(IFormFieldProvider)
class IEvento(model.Schema):
    """Marker inteerface for content type Evento"""

    descrizione_estesa = BlocksField(
        title=_("event_descrizione_estesa", default="Cosa è"),
        required=True,
        description=_(
            "evento_descrizione_estesa_help",
            default="Descrizione dettagliata e completa.",
        ),
    )

    descrizione_destinatari = BlocksField(
        title=_("a_chi_si_rivolge_label", default="A chi è rivolto"),
        required=True,
        description=_(
            "a_chi_si_rivolge_help",
            default="Descrizione testuale dei principali destinatari dell'Evento",
        ),
    )

    prezzo = BlocksField(
        title=_("prezzo", default="Costo"),
        required=True,
        description=_(
            "prezzo_help",
            default="Eventuale costo dell'evento (se ci sono uno o più biglietti), "
            "con link all'acquisto se disponibile",
        ),
    )

    # campi presenti nelle vecchie grafiche che abbiamo deciso di continuare a mostrare
    organizzato_da_interno = RelationList(
        title=_("organizzato_da_interno_label", default="Organizzato da"),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
        description=_(
            "organizzato_da_interno_help",
            default="Indicazione di chi ha organizzato l'evento. Se si tratta di un'Unità organizzativa dell'ASL, includere collegamento alla relativa pagina.",  # noqa
        ),
    )
    organizzato_da_esterno = BlocksField(
        title=_("organizzato_da_esterno_label", default="Organizzatore"),
        required=False,
        description=_(
            "organizzato_da_esterno_help",
            default="Se l'evento non è organizzato direttamente dal comune oppure ha anche un organizzatore esterno,"  # noqa
            " indicare il nome del contatto.",
        ),
    )

    #  campi aggiunti con il pnrr
    patrocinato_da = BlocksField(
        title=_("patrocinato_da_label", default="Patrocinato da"),
        required=False,
        description=_(
            "patrocinato_da_help",
            default="Indicare l'ente che supporta l'evento, se presente.",
        ),
    )

    sponsor = BlocksField(
        title=_("sponsor_label", default="Sponsor"),
        required=False,
        description=_(
            "sponsor_help",
            default="Lista degli sponsor dell'evento.",
        ),
    )

    persone_amministrazione = RelationList(
        title=_("parteciperanno_label", default="Parteciperanno (Persone)"),
        required=False,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        description=_(
            "parteciperanno_help",
            default="Link a persone dell'amministrazione che interverranno all'evento",
        ),
    )

    chi_partecipa = BlocksField(
        title=_("chi_partecipa_label", default="Parteciperanno"),
        required=True,
        description=_(
            "chi_partecipa_help",
            default="Descrizione testuale dei principali partecipanti.",
        ),
    )

    evento_genitore = RelationList(
        title="Fa parte di",
        default=[],
        description=_(
            "evento_genitore_help",
            default='Un evento può essere parte di un altro evento definito come "genitore"',
        ),
        value_type=RelationChoice(
            title=_("Event"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    appuntamenti = RelationList(
        title="Appuntamenti",
        default=[],
        description=_(
            "appuntamenti_help",
            default="Link agli eventi figlio (solo se l'evento in questione è evento genitore).",
        ),
        value_type=RelationChoice(
            title=_("Event"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    strutture = RelationList(
        title="Strutture",
        default=[],
        required=True,
        description=_(
            "strutture_help",
            default="Link all'eventuale scheda della struttura dell'ASL in cui si svolge l'evento.",
        ),
        value_type=RelationChoice(
            title=_("Struttura"), vocabulary="plone.app.vocabularies.Catalog"
        ),
    )

    documenti_correlati = RelationList(
        title="Documenti correlati",
        default=[],
        required=False,
        description=_(
            "documenti_correlati_help",
            default="Link alle schede documenti e allegati di supporto all'evento. Per poter scaricare direttamente un file occorre inserirlo all'interno della cartella 'Allegati'.",
        ),
        value_type=RelationChoice(
            title=_("Documento"), vocabulary="plone.app.vocabularies.Catalog"
        ),
    )

    eventi_correlati = RelationList(
        title="Eventi correlati",
        default=[],
        required=False,
        description=_(
            "eventi_correlati_help", default="Seleziona gli eventi correlati."
        ),
        value_type=RelationChoice(
            title=_("Event"), vocabulary="plone.app.vocabularies.Catalog"
        ),
    )

    parliamo_di = schema.Choice(
        title=_("parliamo_di_label", default="Parliamo di"),
        description=_(
            "parliamo_di_help",
            default="",
        ),
        vocabulary="collective.taxonomy.tipologia_argomento",
        required=False,
        default="",
    )

    informazioni_aggiuntive_luogo = BlocksField(
        title=_(
            "informazioni_aggiuntive_luogo_label", default="Informazioni aggiuntive"
        ),
        required=False,
        description=_(
            "informazioni_aggiuntive_luogo_help",
            default="Informazioni aggiuntivie sul luogo.",
        ),
    )

    # custom widgets

    form.widget(
        "organizzato_da_interno",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["Persona", "UnitaOrganizzativa", "Servizio"],
        },
    )
    form.widget(
        "persone_amministrazione",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["Persona"],
        },
    )

    # custom fieldsets and order
    # form.order_before(sottotitolo="ILeadImageBehavior.image")

    model.fieldset(
        "cose",
        label=_("cose_label", default="Cos'è"),
        fields=[
            "descrizione_estesa",
            "descrizione_destinatari",
        ],
    )

    model.fieldset("costi", label=_("costi_label", default="Costi"), fields=["prezzo"])
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=[
            "organizzato_da_interno",
            "organizzato_da_esterno",
            "patrocinato_da",
            "sponsor",
        ],
    )
    model.fieldset(
        "partecipanti",
        label=_("partecipanti_label", default="Chi partecipa"),
        fields=["chi_partecipa", "persone_amministrazione"],
    )
    model.fieldset(
        "categorization",
        label=_("evento_genitore_label", default="Categorizzazione"),
        fields=["evento_genitore"],
    )
    model.fieldset(
        "categorization",
        label=_("appuntamenti_label", default="Categorizzazione"),
        fields=["appuntamenti"],
    )

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["eventi_correlati", "documenti_correlati"],
    )
    model.fieldset(
        "dove",
        label=_("dove_label", default="Dove"),
        fields=[
            "strutture",
            "informazioni_aggiuntive_luogo",
        ],
    )

    textindexer.searchable("descrizione_estesa")


@implementer(IEvento)
@adapter(IDexterityContent)
class Evento(object):
    """ """

    def __init__(self, context):
        self.context = context
