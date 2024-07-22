from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel.interfaces import ISchemaPlugin
from zope.component import adapter
from zope.interface import implementer


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

    def set_description_required(self):
        """fix Documento fields"""
        if self.schema.getName() == "IBasic":
            self.schema["description"].required = True
