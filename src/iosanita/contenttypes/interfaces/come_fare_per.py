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
        title=_("a_chi_si_rivolge_label", default="A chi si rivolge"),
        required=True,
        description=_(
            "come_fare_a_chi_si_rivolge_help",
            default="A chi si rivolge questo servizio.",
        ),
    )

    model.fieldset(
        "utenti",
        label=_("utenti_label", default="Utenti"),
        fields=[
            "a_chi_si_rivolge",
        ],
    )
    # model.fieldset(
    #     "informazioni",
    #     label=_("informazioni_label", default="Ulteriori informazioni"),
    #     fields=[
    #         "parliamo_di",
    #     ],
    # )
