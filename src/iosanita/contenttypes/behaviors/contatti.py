# -*- coding: utf-8 -*-
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from plone.app.dexterity import textindexer
from collective.volto.blocksfield.field import BlocksField

from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces.persona import IPersona

from iosanita.contenttypes.interfaces.unita_organizzativa import IUnitaOrganizzativa


@provider(IFormFieldProvider)
class IContattiUnitaOrganizzativa(model.Schema):
    contact_info = RelationList(
        title=_(
            "contact_unita_organizzativa_info_label",
            default="Punti di contatto dell'unità organizzativa",
        ),
        description=_(
            "contact_unita_organizzativa_info_help",
            default="Contatti dell'unità organizzativa.",
        ),
        required=True,
        default=[],
        value_type=RelationChoice(
            title=_("Informazioni di contatto"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
    )
    orario_pubblico = BlocksField(
        title=_("orario_pubblico_label", default="Orario per il pubblico"),
        description=_(
            "orario_pubblico_help",
            default="Indicare eventuali orari di accesso al pubblico",
        ),
        required=True,
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
        fields=["contact_info", "orario_pubblico"],
    )

    textindexer.searchable("orario_pubblico")



@provider(IFormFieldProvider)
class IContattiPersona(model.Schema):
    contact_info = RelationList(
        title=_(
            "contatti_event_contact_info_label",
            default="Punti di contatto",
        ),
        description=_(
            "contact_info_help",
            default="Punti di contatto della persona.",
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


@provider(IFormFieldProvider)
class IContattiStep(model.Schema):
    contact_info = RelationList(
        title=_(
            "contatti_persona_contact_info_label",
            default="Punti di contatto",
        ),
        description=_(
            "contact_info_help",
            default="Punti di contatto per questo passo.",
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


@provider(IFormFieldProvider)
class IContattiStruttura(model.Schema):
    contact_info = RelationList(
        title=_(
            "contatti_struttura_contact_info_label",
            default="Punti di contatto",
        ),
        description=_(
            "contact_info_help",
            default="Punti di contatto.",
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


@implementer(IContattiUnitaOrganizzativa)
@adapter(IUnitaOrganizzativa)
class ContattiUnitaOrganizzativa(object):
    """ """

    def __init__(self, context):
        self.context = context


@implementer(IContattiStep)
@adapter(IContattiStep)
class ContattiStep(object):
    """ """

    def __init__(self, context):
        self.context = context



@implementer(IContattiPersona)
@adapter(IPersona)
class ContattiPersona(object):
    """ """

    def __init__(self, context):
        self.context = context


@implementer(IContattiStruttura)
@adapter(IContattiStruttura)
class ContattiStruttura(object):
    """ """

    def __init__(self, context):
        self.context = context
