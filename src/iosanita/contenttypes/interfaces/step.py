# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces import IIosanitaContenttypes
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList


class IStep(model.Schema, IIosanitaContenttypes):
    """Marker interface for content type Step"""

    testo = BlocksField(
        title=_("testo_label", default="Testo"),
        description=_(
            "testo_help",
            default="Descrizione del passo della procedura.",
        ),
        required=False,
    )
    uo_correlata = RelationList(
        title=_("uo_correlata_step_label", default="Dove"),
        description=_(
            "uo_correlata_step_help",
            default="Seleziona una Unità organizzativa.",
        ),
        default=[],
        value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
        required=True,
    )

    form.widget(
        "uo_correlata",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )
