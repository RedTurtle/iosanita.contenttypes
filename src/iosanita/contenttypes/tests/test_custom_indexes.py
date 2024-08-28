# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from iosanita.contenttypes.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.testing import RelativeSession
from zope.component import getMultiAdapter
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from plone.app.dexterity.behaviors.metadata import IDublinCore
from zope.lifecycleevent import Attributes

import unittest


class TestCustomIndexes(unittest.TestCase):
    """"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_parent_metadata_has_parent_data(self):
        parent = api.content.create(
            container=self.portal,
            type="Document",
            title="Parent",
        )

        child = api.content.create(
            container=parent,
            type="Document",
            title="Child",
        )

        brain = api.content.find(UID=child.UID())[0]

        self.assertEqual(
            sorted(["title", "UID", "@id", "@type"]), sorted(list(brain.parent.keys()))
        )
        self.assertEqual(brain.parent["title"], "Parent")
        self.assertEqual(brain.parent["UID"], parent.UID())

    def test_when_parent_changes_children_will_be_updated(self):
        parent = api.content.create(
            container=self.portal,
            type="Document",
            title="Parent",
        )

        child = api.content.create(
            container=parent,
            type="Document",
            title="Child",
        )

        brain = api.content.find(UID=child.UID())[0]
        self.assertEqual(brain.parent["title"], "Parent")

        # update title
        parent.title = "New Parent Title"
        descriptions = [Attributes(IDublinCore, *["IDublinCore.title"])]
        notify(ObjectModifiedEvent(parent, *descriptions))

        brain = api.content.find(UID=child.UID())[0]
        self.assertEqual(brain.parent["title"], "New Parent Title")
