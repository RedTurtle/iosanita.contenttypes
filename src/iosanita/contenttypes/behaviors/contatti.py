# -*- coding: utf-8 -*-
from iosanita.contenttypes import _
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
class IContattiEvent(model.Schema):
    contact_info = RelationList(
        title=_(
            "contact_info_label",
            default="Punti di contatto",
        ),
        description=_(
            "contact_info_help",
            default="Relazione con i punti di contatto dell'evento.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Punti di contatto"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "contact_info",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["PuntoDiContatto"],
        },
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["contact_info"],
    )


@implementer(IContattiEvent)
@adapter(IContattiEvent)
class ContattiEvent(object):
    """ """

    def __init__(self, context):
        self.context = context
