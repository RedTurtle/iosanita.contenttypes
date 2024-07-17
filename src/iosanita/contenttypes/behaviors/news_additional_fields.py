# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from plone.app.contenttypes.interfaces import INewsItem
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class INewsAdditionalFields(model.Schema):
    descrizione_estesa = BlocksField(
        title=_(
            "new_additional_fields_descrizione_estesa", default="Descrizione estesa"
        ),
        required=True,
        description=_(
            "new_additional_fields_descrizione_estesa_help",
            default="Descrizione dettagliata e completa.",
        ),
    )

    numero_progressivo_cs = schema.TextLine(
        title=_(
            "numero_progressivo_cs_label",
            default="Numero progressivo del comunicato stampa",
        ),
        description=_(
            "numero_progressivo_cs_help",
            default="Se è un comunicato stampa, indicare un'eventuale numero progressivo del comunicato stampa.",
        ),
        required=False,
    )

    a_cura_di = RelationList(
        title=_("a_cura_di_label", default="A cura di"),
        description=_(
            "a_cura_di_help",
            default="Seleziona l'ufficio di comunicazione responsabile di "
            "questa notizia/comunicato stampa.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    )

    a_cura_di_persone = RelationList(
        title=_("a_cura_di_persone_label", default="Persone"),
        description=_(
            "a_cura_di_persone_help",
            default="Elenco delle persone dell'ASL citate nella notizia, con collegamento alle relative pagine foglia persona. L'elemento è necessario se nella notizia sono citate persone dell'ASL che hanno una pagina persona.",
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
    )

    notizie_correlate = RelationList(
        title=_("notizie_correlate_label", default="Notizie correlate"),
        description=_(
            "notizie_correlate_help",
            default="Elenco di altre notizie simili o collegate, con collegamento alle relative pagine foglia notizia.",
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
    )

    servizi_correlati = RelationList(
        title=_("servizi_correlati_label", default="Servizi e prestazioni"),
        description=_(
            "servizi_correlati_help",
            default="Elenco dei servizi e delle prestazioni dell'ASL citati nella notizia, con collegamento alle relative pagine foglia servizio. L'elemento è necessario se nella notizia sono citati specifici servizi o prestazioni dell'ASL.",
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
    )

    strutture_correlate = RelationList(
        title=_("strutture_correlate_label", default="Strutture correlate"),
        description=_(
            "strutture_correlate_help",
            default="Elenco delle strutture dell'ASL citate nella notizia, con collegamento alle relative pagine foglia struttura. L'elemento è necessario se nella notizia sono citate strutture dell'ASL.",
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=False,
    )

    documenti = RelationList(
        title="Documenti",
        default=[],
        description=_(
            "documenti_help",
            default="Elenco dei documenti correlati, con collegamento alle relative pagine foglia documento (se documenti ufficiali dell'ASL) o download diretto degli allegati.",
        ),
        value_type=RelationChoice(
            title=_("Documento"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    # custom widgets
    form.widget(
        "a_cura_di",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )
    form.widget(
        "a_cura_di_persone",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["Persona"],
        },
    )
    form.widget(
        "notizie_correlate",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["News Item"],
        },
    )
    form.widget(
        "servizi_correlati",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["Servizio"],
        },
    )
    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=[
            "a_cura_di_persone",
            "notizie_correlate",
            "servizi_correlati",
            "strutture_correlate",
            "documenti",
        ],
    )
    # custom fieldsets and order
    form.order_before(descrizione_estesa="ILeadImageBehavior.image")
    form.order_before(numero_progressivo_cs="ILeadImageBehavior.image")
    form.order_before(a_cura_di="ILeadImageBehavior.image")

    textindexer.searchable("descrizione_estesa")


@implementer(INewsAdditionalFields)
@adapter(INewsItem)
class NewsAdditionalFields(object):
    """ """

    def __init__(self, context):
        self.context = context
