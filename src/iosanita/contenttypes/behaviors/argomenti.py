# -*- coding: utf-8 -*-
from iosanita.contenttypes import _
from plone.app.contenttypes.interfaces import IEvent, INewsItem
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


class IArgomentiSchema(model.Schema):
    """Marker interface for Argomenti"""

    tassonomia_argomenti = RelationList(
        title=_("tassonomia_argomenti_label", default="Argomenti"),
        description=_(
            "tassonomia_argomenti_help",
            default="Seleziona una lista di argomenti d'interesse per questo"
            " contenuto.",
        ),
        value_type=RelationChoice(
            title=_("Argomenti correlati"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        default=[],
    )

    form.widget(
        "tassonomia_argomenti",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["Pagina Argomento"],
        },
    )

    textindexer.searchable("tassonomia_argomenti")


@provider(IFormFieldProvider)
class IArgomenti(IArgomentiSchema):
    """ """


@provider(IFormFieldProvider)
class IArgomentiEvento(IArgomentiSchema):
    """ """

    tassonomia_argomenti = RelationList(
        title=_("tassonomia_argomenti_label", default="Argomenti"),
        description=_(
            "tassonomia_argomenti_help",
            default="Seleziona una lista di argomenti d'interesse per questo"
            " contenuto.",
        ),
        value_type=RelationChoice(
            title=_("Argomenti correlati"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=True,
        default=[],
    )


@provider(IFormFieldProvider)
class IArgomentiNews(IArgomentiSchema):
    """ """

    tassonomia_argomenti = RelationList(
        title=_("tassonomia_argomenti_label", default="Argomenti"),
        description=_(
            "tassonomia_argomenti_help",
            default="Seleziona una lista di argomenti d'interesse per questo"
            " contenuto.",
        ),
        value_type=RelationChoice(
            title=_("Argomenti correlati"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=True,
        default=[],
    )


@implementer(IArgomenti)
@adapter(IDexterityContent)
class Argomenti(object):
    """"""

    def __init__(self, context):
        self.context = context


@implementer(IArgomentiEvento)
@adapter(IEvent)
class ArgomentiEvento(object):
    """"""

    def __init__(self, context):
        self.context = context


@implementer(IArgomentiNews)
@adapter(INewsItem)
class ArgomentiNews(object):
    """"""

    def __init__(self, context):
        self.context = context
