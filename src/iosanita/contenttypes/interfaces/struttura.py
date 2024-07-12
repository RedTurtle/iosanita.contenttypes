# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces import IIosanitaContenttypes

from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


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
        title=_("event_descrizione_estesa", default="Cosa è"),
        required=False,
        description=_(
            "evento_descrizione_estesa_help",
            default="Descrizione più estesa della struttura con riferimento alle principali attività sanitarie svolte.",
        ),
    )

    a_chi_si_rivolge = BlocksField(
        title=_("a_chi_si_rivolge_label", default="A chi è rivolto"),
        required=True,
        description=_(
            "a_chi_si_rivolge_help",
            default="Descrizione testuale degli utenti dell'ASL a cui è rivolta la struttura.",
        ),
    )

    parliamo_di = schema.List(
        title=_("parliamo_di_label", default="Parliamo di"),
        description=_(
            "parliamo_di_help",
            default="Indicazioni degli argomenti con cui il contenuto di pagina viene taggato.",
        ),
        value_type=schema.Choice(
            vocabulary="collective.taxonomy.tipologia_argomento",
        ),
        required=False,
    )

    come_accedere = BlocksField(
        title=_("come_accedere", default="Come accedere"),
        required=True,
        description=_(
            "come_accedere_help",
            default="Modalità di accesso alla struttura con particolare attenzione agli accessi per disabili ed eventuale descrizione di come arrivare, costi e regole di accesso.",
        ),
    )

    orari_apertura = BlocksField(
        title=_("orari_apertura", default="Orari di apertura"),
        required=True,
        description=_(
            "orari_apertura_help",
            default="Orario di apertura della struttura al pubblico.",
        ),
    )

    responsabile_struttura = RelationList(
        title=_(
            "responsabile_struttura_label",
            default="Responsabile struttura",
        ),
        description=_(
            "responsabile_struttura_help",
            default="La persona che dirige la struttura, con collegamento alla relativa pagina foglia persona.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Persona"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    coordinatore_struttura = RelationList(
        title=_(
            "coordinatore_struttura_label",
            default="Coordinatore struttura",
        ),
        description=_(
            "responsabile_struttura_help",
            default="La persona che coordina la struttura, con collegamento alla relativa pagina foglia persona.",
        ),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_("Persona"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )

    strutture_correlate = RelationList(
        title="Strutture correlate",
        default=[],
        value_type=RelationChoice(
            title=_("Struttura correlata"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        missing_value=(),
        description=_(
            "strutture_correlate_help",
            default="Elenco di altre strutture simili o collegate.",
        ),
    )
    form.widget(
        "strutture_correlate",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["Struttura"],
        },
    )

    form.widget(
        "responsabile_struttura",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["Persona"],
        },
    )

    model.fieldset(
        "utenti",
        label=_("utenti_label", default="Utenti"),
        fields=[
            "a_chi_si_rivolge",
        ],
    )
    model.fieldset(
        "informazioni",
        label=_("informazioni_label", default="Ulteriori informazioni"),
        fields=[
            "parliamo_di",
        ],
    )
    model.fieldset(
        "correlati",
        label=_("sturetture_correlate_struttura_label", default="Contenuti collegati"),
        fields=["strutture_correlate"],
    )
