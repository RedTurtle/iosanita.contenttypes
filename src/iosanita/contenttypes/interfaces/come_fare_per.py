# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces import IIosanitaContenttypes

# from plone.app.z3cform.widget import RelatedItemsFieldWidget
# from plone.autoform import directives as form
from plone.namedfile import field
from plone.supermodel import model

# from z3c.relationfield.schema import RelationChoice
# from z3c.relationfield.schema import RelationList
from zope import schema


class IComeFarePer(model.Schema, IIosanitaContenttypes):
    """Marker interface for content type Servizio"""

    sottotitolo = schema.TextLine(
        title=_("sottotitolo_label", default="Sottotitolo"),
        description=_(
            "sottotitolo_help",
            default="Indica un eventuale sottotitolo/titolo alternativo.",
        ),
        required=False,
    )

    immagine_tema = field.NamedBlobImage(
        title=_("immagine_tema_label", default="Immagine del tema"),
        required=False,
        description=_(
            "immagine_tema_help",
            default="Immagine del tema trattato.",
        ),
    )

    descrizione_estesa = BlocksField(
        title=_("descrizione_estesa_label", default="Panoramica"),
        description=_(
            "descrizione_estesa_help",
            default="Descrizione estesa.",
        ),
        required=True,
    )

    a_chi_si_rivolge = BlocksField(
        title=_("a_chi_si_rivolge_label", default="A chi è rivolto"),
        required=True,
        description=_(
            "a_chi_si_rivolge_help",
            default="A chi si rivolge questo servizio.",
        ),
    )

    come_si_fa = BlocksField(
        title=_("come_si_fa_label", default="Come fare"),
        required=True,
        description=_(
            "come_si_fa_help",
            default="Descrizione della procedura da seguire per poter"
            " usufruire del servizio.",
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

    ultimo_aggiornamento = schema.Date(
        title=_("ultimo_aggiornamento_label", default="Ultimo aggiornamento"),
        required=True,
        description=_(
            "ultimo_aggiornamento_help",
            default="Data in cui è stato effettuato l'ultimo aggiornamento ai contenuti della pagina.",
        ),
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
