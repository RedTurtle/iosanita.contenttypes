# -*- coding: utf-8 -*-
from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces.step import IStep
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider



@provider(IFormFieldProvider)
class IContattiStep(model.Schema):
    contact_info = RelationList(
        title=_(
            "contact_info_label",
            default="Contatti",
        ),
        description=_(
            "contact_info_help",
            default="I contatti per questo step.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Contatti"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    # form.widget(
    #     "contact_info",
    #     RelatedItemsFieldWidget,
    #     vocabulary="plone.app.vocabularies.Catalog",
    #     pattern_options={
    #         "selectableTypes": ["PuntoDiContatto"],
    #     },
    # )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["contact_info"],
    )


@implementer(IContattiStep)
@adapter(IStep)
class ContattiStep(object):
    """ """

    def __init__(self, context):
        self.context = context
