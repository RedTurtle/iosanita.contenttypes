from iosanita.contenttypes.interfaces import IIosanitaContenttypesLayer
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.serializer.relationfield import (
    RelationListFieldSerializer as BaseSerializer,
)
from z3c.relationfield.interfaces import IRelationList
from zope.component import adapter
from zope.interface import implementer


@adapter(IRelationList, IDexterityContent, IIosanitaContenttypesLayer)
@implementer(IFieldSerializer)
class RelationListFieldSerializer(BaseSerializer):

    def get_value(self, default=None):
        """
        Return a list of relations that the user has permission to view.
        """
        value = super().get_value()
        can_edit = api.user.has_permission("Modify portal content", obj=self.context)
        if value:
            # Only include relations that still resolve (skip broken relations
            # e.g. when the target content was deleted). Avoids [null] in JSON.
            relations = []
            # THIS IS THE PATCH (plone.restapi >= 10.0.0rc1 introduced the to_object check)
            for rel in value:
                rel_object = rel.to_object
                if not rel_object:
                    continue
                can_view_rel = api.user.has_permission("View", obj=rel_object)
                if can_edit or can_view_rel:
                    relations.append(rel)
            return relations
            # END OF PATCH
        if default is None:
            return []
        return default
