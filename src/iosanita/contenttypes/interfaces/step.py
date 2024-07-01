# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces import IIosanitaContenttypes
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.namedfile import field
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


class IStep(model.Schema, IIosanitaContenttypes):
    """Marker interface for content type Servizio"""


    testo = BlocksField(
        title=_("testo_label", default="Testo"),
        description=_(
            "testo_help",
            default="Descrizione del passo della procedura.",
        ),
        required=False,
    )

    dove = RelationList(
        title="Dove",
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=True,
        description=_(
            "dove_help",
            default="Seleziona una struttura o punto di contatto.",
        ),
    )

    documenti = RelationList(
        title="Documenti",
        default=[],
        description=_(
            "documenti_help",
            default="Seleziona la lista dei documenti di supporto.",
        ),
        value_type=RelationChoice(
            title=_("Documento"), vocabulary="plone.app.vocabularies.Catalog"
        ),
        required=False,
    )

    
    # form.widget(
    #     "dove",
    #     RelatedItemsFieldWidget,
    #     vocabulary="plone.app.vocabularies.Catalog",
    #     pattern_options={
    #         "selectableTypes": ["UnitaOrganizzativa"],
    #     },
    # )
    # form.widget(
    #     "documenti",
    #     RelatedItemsFieldWidget,
    #     vocabulary="plone.app.vocabularies.Catalog",
    #     pattern_options={"selectableTypes": ["Documento"]},
    # )

