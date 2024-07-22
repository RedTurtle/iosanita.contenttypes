# -*- coding: utf-8 -*-
from iosanita.contenttypes import _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IServizi(model.Schema):
    """Marker interface"""

    servizi = RelationList(
        title=_("servizi_label", default="Servizi"),
        default=[],
        value_type=RelationChoice(
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        missing_value=(),
        description=_(
            "servizi_help",
            default="Elenco dei servizi e delle prestazioni offerti.",
        ),
    )
    form.widget(
        "servizi",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"selectableTypes": ["Servizio"]},
    )
    model.fieldset(
        "servizi",
        label=_("servizi_label", default="Servizi"),
        fields=["servizi"],
    )


@implementer(IServizi)
@adapter(IDexterityContent)
class Servizi(object):
    """"""

    def __init__(self, context):
        self.context = context
