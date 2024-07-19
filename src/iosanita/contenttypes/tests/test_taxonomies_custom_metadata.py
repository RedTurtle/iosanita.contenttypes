# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from iosanita.contenttypes.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.event import notify
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent

import unittest


class TestTaxonomiesCustomMetadata(unittest.TestCase):
    """"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_parliamo_di_metadata_has_array_of_objects(self):
        """ """
        struttura = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Test servizio",
            parliamo_di=["vaccinazioni-anti-covid-19", "igiene-pubblica"],
        )
        res = api.content.find(UID=struttura.UID())

        self.assertEqual(len(res), 1)
        self.assertEqual(
            res[0].parliamo_di, ["vaccinazioni-anti-covid-19", "igiene-pubblica"]
        )
        self.assertEqual(res[0].parliamo_di_metadata, [])
