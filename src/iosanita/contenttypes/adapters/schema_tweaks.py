from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.interfaces import OMITTED_KEY
from plone.supermodel.interfaces import ISchemaPlugin
from redturtle.bandi.interfaces.bandoSchema import IBandoSchema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISchemaPlugin)
@adapter(IFormFieldProvider)
class SchemaTweaks(object):
    """
    Fix fields for content-types to be like v2 of design.plone.contenttypes
    """

    order = 99999

    def __init__(self, schema):
        self.schema = schema

    def __call__(self):
        self.set_description_required()
        self.fix_bando()

    def set_description_required(self):
        """fix Documento fields"""
        if self.schema.getName() == "IBasic":
            self.schema["description"].required = True

    def fix_bando(self):
        """fix Bando fields"""
        IBandoSchema["destinatari"].required = False
        IBandoSchema.setTaggedValue(
            OMITTED_KEY,
            [
                (Interface, "riferimenti_bando", "true"),
                (Interface, "ente_bando", "true"),
                (Interface, "destinatari", "true"),
            ],
        )
