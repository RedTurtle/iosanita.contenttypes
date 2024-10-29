from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.interfaces import OMITTED_KEY
from plone.supermodel.interfaces import ISchemaPlugin
from redturtle.bandi.interfaces.bandoSchema import IBandoSchema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import os


@implementer(ISchemaPlugin)
@adapter(IFormFieldProvider)
class SchemaTweaks(object):
    """ """

    order = 99999

    def __init__(self, schema):
        self.schema = schema

    def __call__(self):
        self.set_description_required()
        self.fix_bando()
        self.set_dove_fields_required()

    def set_description_required(self):
        """fix Documento fields"""
        if os.environ.get("DISABLE_DESCRIPTION_VALIDATION", False):
            return
        if self.schema.getName() == "IBasic":
            self.schema["description"].required = True

    def fix_bando(self):
        """fix Bando fields"""
        if self.schema.getName() == "IBando":
            # set it only once
            IBandoSchema["destinatari"].required = False
            IBandoSchema["scadenza_bando"].required = True
            IBandoSchema.setTaggedValue(
                OMITTED_KEY,
                [(Interface, "destinatari", "true")],
            )

    def set_dove_fields_required(self):
        """fix Dove fields"""
        if os.environ.get("DISABLE_DESCRIPTION_VALIDATION", False):
            return
        if self.schema.getName() == "IAddress":
            self.schema["street"].required = True
            self.schema["zip_code"].required = True
            self.schema["city"].required = True
            self.schema["country"].required = True
