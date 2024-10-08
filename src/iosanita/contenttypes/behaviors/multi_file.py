# -*- coding: utf-8 -*-
from iosanita.contenttypes import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


class IMultiFileSchema(model.Schema):
    """"""

    file = field.NamedBlobFile(
        title=_("file_label", default="File principale"),
        description=_(
            "file_help",
            default="Inserisci il file principale di questo contenuto.",
        ),
        required=True,
    )

    formato_alternativo_1 = field.NamedBlobFile(
        title=_("formato_alternativo_1_label", default="Formato alternativo 1"),
        description=_(
            "formato_alternativo_1_help",
            default="Inserisci un eventuale formato alternativo del "
            "file principale.",
        ),
        required=False,
    )

    formato_alternativo_2 = field.NamedBlobFile(
        title=_("formato_alternativo_2_label", default="Formato alternativo 2"),
        description=_(
            "formato_alternativo_2_help",
            default="Inserisci un eventuale formato alternativo del "
            "file principale.",
        ),
        required=False,
    )

    model.primary("file")

    model.fieldset(
        "formati",
        label=_("formati_label", default="Formati"),
        fields=[
            "file",
            "formato_alternativo_1",
            "formato_alternativo_2",
        ],
    )


@provider(IFormFieldProvider)
class IMultiFile(IMultiFileSchema):
    """"""


@implementer(IMultiFile)
@adapter(IDexterityContent)
class MultiFile(object):
    """"""

    def __init__(self, context):
        self.context = context
