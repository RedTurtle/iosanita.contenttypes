# -*- coding: utf-8 -*-
from iosanita.contenttypes import _
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from plone.dexterity.interfaces import IDexterityContent


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
    correlato_in_evidenza = RelationList(
        title=_("correlato_in_evidenza_label", default="Correlato in evidenza"),
        description=_(
            "correlato_in_evidenza_help",
            default="Seleziona un correlato da mettere in evidenza per questo"
            " contenuto.",
        ),
        value_type=RelationChoice(
            title=_("Correlato in evidenza"),
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
    form.widget(
        "correlato_in_evidenza",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={"maximumSelectionSize": 1},
    )

    textindexer.searchable("tassonomia_argomenti")


@provider(IFormFieldProvider)
class IArgomenti(IArgomentiSchema):
    """ """

    model.fieldset(
        "correlati",
        label=_("correlati_label", default="Contenuti collegati"),
        fields=["correlato_in_evidenza"],
    )


@implementer(IArgomenti)
@adapter(IDexterityContent)
class Argomenti(object):
    """"""

    def __init__(self, context):
        self.context = context