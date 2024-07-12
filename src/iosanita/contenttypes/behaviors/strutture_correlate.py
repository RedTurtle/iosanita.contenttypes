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
class IStruttureCorrelate(model.Schema):
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
            default="Seleziona la lista delle strutture correlate.",
        ),
    )
    form.widget(
        "strutture_correlate",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    model.fieldset(
        "correlati",
        label=_("sturetture_correlate_struttura_label", default="Contenuti collegati"),
        fields=["strutture_correlate"],
    )


@implementer(IStruttureCorrelate)
@adapter(IDexterityContent)
class StruttureCorrelate(object):
    """ """

    def __init__(self, context):
        self.context = context
