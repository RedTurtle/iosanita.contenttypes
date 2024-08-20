# -*- coding: utf-8 -*-
from iosanita.contenttypes import _
from iosanita.contenttypes.controlpanels.settings import IIoSanitaSettings
from plone import api
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


def showModifiedDefaultValue(context=None):
    return api.portal.get_registry_record(
        "show_modified_default", interface=IIoSanitaSettings, default=False
    )


@provider(IFormFieldProvider)
class IShowModified(model.Schema):
    show_modified = schema.Bool(
        title=_("show_modified_label", default="Mostra la data di ultima modifica"),
        description=_(
            "show_modified_help",
            default="Se attivo, verrà mostrata la data di ultima modifica in "
            "visualizzazione del contenuto.",
        ),
        required=False,
        defaultFactory=showModifiedDefaultValue,
    )

    model.fieldset(
        "settings",
        label="Impostazioni",
        fields=["show_modified"],
    )


@implementer(IShowModified)
@adapter(IDexterityContent)
class ShowModified(object):
    """ """

    def __init__(self, context):
        self.context = context
