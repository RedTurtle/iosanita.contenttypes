# -*- coding: utf-8 -*-
from iosanita.contenttypes.testing import RESTAPI_TESTING
from iosanita.contenttypes.upgrades.v1010 import upgrade
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestUpgrade1010(unittest.TestCase):
    layer = RESTAPI_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.bando = api.content.create(
            container=self.portal, type="Bando", title="Bando"
        )
        self.news = api.content.create(
            container=self.portal, type="News Item", title="News"
        )

    def test_existing_subfolders_are_excluded_from_search(self):
        subfolders = [self.bando["graduatoria"], self.news["allegati"]]
        for item in subfolders:
            item.exclude_from_search = False
            item.reindexObject(idxs=["exclude_from_search"])

        upgrade()

        for item in subfolders:
            self.assertTrue(item.exclude_from_search)
            brains = api.content.find(UID=item.UID(), exclude_from_search=True)
            self.assertEqual(len(brains), 1)

    def test_other_contents_are_not_touched(self):
        upgrade()

        self.assertFalse(getattr(self.bando.aq_base, "exclude_from_search", False))
        self.assertFalse(getattr(self.news.aq_base, "exclude_from_search", False))
