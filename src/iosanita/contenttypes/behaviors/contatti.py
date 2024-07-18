# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from plone.app.dexterity import textindexer
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


class IContattiSchema(model.Schema):
    punti_di_contatto = RelationList(
        title=_(
            "punti_di_contatto_label",
            default="Punti di contatto",
        ),
        description=_(
            "punti_di_contatto_help",
            default="Seleziona una lista di punti di contatto.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    form.widget(
        "punti_di_contatto",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["PuntoDiContatto"],
        },
    )
    model.fieldset(
        "contatti",
        label=_("contatti_label", default="Contatti"),
        fields=["punti_di_contatto"],
    )


@provider(IFormFieldProvider)
class IContatti(IContattiSchema):
    """"""


@implementer(IContatti)
@adapter(IDexterityContent)
class Contatti(object):
    """ """

    def __init__(self, context):
        self.context = context
