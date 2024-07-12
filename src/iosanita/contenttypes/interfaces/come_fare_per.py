# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces import IIosanitaContenttypes

# from plone.app.z3cform.widget import RelatedItemsFieldWidget
# from plone.autoform import directives as form
# from plone.namedfile import field
from plone.supermodel import model

# from z3c.relationfield.schema import RelationChoice
# from z3c.relationfield.schema import RelationList
from zope import schema


class IComeFarePer(model.Schema, IIosanitaContenttypes):
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
        title=_("come_fare_per_descrizione_estesa_label", default="Panoramica"),
        description=_(
            "come_fare_per_descrizione_estesa_help",
            default="Descrizione estesa.",
        ),
        required=True,
    )

    a_chi_si_rivolge = BlocksField(
        title=_("a_chi_si_rivolge_label", default="A chi è rivolto"),
        required=True,
        description=_(
            "come_fare_a_chi_si_rivolge_help",
            default="A chi si rivolge questo servizio.",
        ),
    )

    # costi_vincoli = schema.Text(
    #     title=_("costi_vincoli_label", default="Costi e vincoli"),
    #     required=False,
    #     description=_(
    #         "costi_vincoli_help",
    #         default="Descrizione delle condizioni e dei termini economici e dei vincoli per"
    #         " completare la procedura di richiesta del servizio.",
    #     ),
    # )

    # tempistiche = schema.Text(
    #     title=_("tempistiche_label", default="Tempistiche"),
    #     required=False,
    #     description=_(
    #         "tempistiche_help",
    #         default="Descrivere le informazioni dettagliate riguardo eventuali tempi"
    #         " e scadenze.",
    #     ),
    # )

    # dove_rivolgersi = RelationList(
    #     title="Dove rivolgersi",
    #     default=[],
    #     value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    #     required=True,
    #     description=_(
    #         "dove_rivolgersi_help",
    #         default="Seleziona una lista delle sedi e dei luoghi in cui è presente"
    #         " questo servizio.",
    #     ),
    # )

    # altri_documenti = RelationList(
    #     title="Documenti",
    #     default=[],
    #     description=_(
    #         "altri_documenti_help",
    #         default="Seleziona la lista dei documenti di supporto collegati"
    #         " a questo servizio.",
    #     ),
    #     value_type=RelationChoice(
    #         title=_("Documento"), vocabulary="plone.app.vocabularies.Catalog"
    #     ),
    #     required=False,
    # )

    parliamo_di = schema.List(
        title=_("parliamo_di_label", default="Parliamo di"),
        description=_(
            "come_fare_per_parliamo_di_help",
            default="Indicazioni degli argomenti con cui il contenuto di pagina viene taggato.",
        ),
        value_type=schema.Choice(
            vocabulary="collective.taxonomy.tipologia_argomento",
        ),
        required=False,
    )

    # form.widget(
    #     "dove_rivolgersi",
    #     RelatedItemsFieldWidget,
    #     vocabulary="plone.app.vocabularies.Catalog",
    #     pattern_options={
    #         "selectableTypes": ["UnitaOrganizzativa"],
    #     },
    # )
    # form.widget(
    #     "altri_documenti",
    #     RelatedItemsFieldWidget,
    #     vocabulary="plone.app.vocabularies.Catalog",
    #     pattern_options={"selectableTypes": ["Documento"]},
    # )

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
