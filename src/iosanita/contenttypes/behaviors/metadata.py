from plone.app.dexterity import _
from plone.app.dexterity.behaviors.metadata import Basic
from zope import schema
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import provider
from plone.supermodel import model
from plone.autoform import directives
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm


@provider(IFormFieldProvider)
class IIoSanitaBasic(model.Schema):
    """
    Make description required
    """

    # default fieldset
    title = schema.TextLine(title=_("label_title", default="Title"), required=True)

    description = schema.Text(
        title=_("label_description", default="Summary"),
        description=_(
            "help_description", default="Used in item listings and search results."
        ),
        required=True,
        missing_value="",
    )

    directives.order_before(description="*")
    directives.order_before(title="*")

    directives.omitted("title", "description")
    directives.no_omit(IEditForm, "title", "description")
    directives.no_omit(IAddForm, "title", "description")


class IoSanitaBasic(Basic):
    """ """
