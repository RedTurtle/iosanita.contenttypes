# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from iosanita.contenttypes.testing import RESTAPI_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.testing import RelativeSession
from zope.component import getMultiAdapter

import os
import unittest


class TestBandoSerializer(unittest.TestCase):
    """"""

    layer = RESTAPI_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.bando = api.content.create(
            container=self.portal, type="Bando", title="Bando"
        )

    def tearDown(self):
        self.api_session.close()

    def test_stato_bando_info_in_serialzier(self):
        serializer = getMultiAdapter((self.bando, self.request), ISerializeToJson)()

        self.assertIn("stato_bando", serializer)

    def test_approfondimenti_info_in_serializer(self):
        serializer = getMultiAdapter((self.bando, self.request), ISerializeToJson)()

        self.assertIn("approfondimenti", serializer)

    def test_approfondimenti_data(self):
        # empty if no files in some bando children
        serializer = getMultiAdapter((self.bando, self.request), ISerializeToJson)()

        self.assertEqual(serializer["approfondimenti"], [])

        # now fill one folder
        filename = os.path.join(os.path.dirname(__file__), "example.txt")
        api.content.create(
            container=self.bando["documenti"],
            type="File",
            title="attachment",
            file=NamedBlobFile(
                data=open(filename, "rb").read(),
                filename="example.txt",
                contentType="text/plain",
            ),
        )

        serializer = getMultiAdapter((self.bando, self.request), ISerializeToJson)()

        self.assertEqual(len(serializer["approfondimenti"]), 1)
        self.assertEqual(serializer["approfondimenti"][0]["title"], "Documenti")
        self.assertEqual(len(serializer["approfondimenti"][0]["children"]), 1)
        self.assertEqual(
            serializer["approfondimenti"][0]["children"][0]["title"], "attachment"
        )
