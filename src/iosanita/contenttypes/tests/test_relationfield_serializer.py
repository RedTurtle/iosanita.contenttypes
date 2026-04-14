# -*- coding: utf-8 -*-
"""Setup tests for this package."""

from iosanita.contenttypes.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.restapi.interfaces import ISerializeToJson
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.event import notify
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent

import unittest


class TestRelationFieldSerializer(unittest.TestCase):
    """"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        intids = getUtility(IIntIds)

        self.persona_private = api.content.create(
            container=self.portal, type="Persona", title="Private"
        )
        self.persona_published = api.content.create(
            container=self.portal, type="Persona", title="Published"
        )

        api.content.transition(self.persona_published, to_state="published")

        self.uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="uo",
            personale_correlato=[
                RelationValue(intids.getId(self.persona_published)),
                RelationValue(intids.getId(self.persona_private)),
            ],
        )
        notify(ObjectModifiedEvent(self.uo))

    def test_uo_serializer_return_all_persone_for_manager(self):
        """ """
        serializer = queryMultiAdapter((self.uo, self.request), ISerializeToJson)()

        self.assertEqual(len(serializer["personale_correlato"]), 2)

    def test_uo_serializer_return_only_published_persona_for_anonymous(self):
        """ """
        logout()
        serializer = queryMultiAdapter((self.uo, self.request), ISerializeToJson)()

        self.assertEqual(len(serializer["personale_correlato"]), 1)
        self.assertEqual(
            serializer["personale_correlato"][0]["UID"], self.persona_published.UID()
        )
