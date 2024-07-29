# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from iosanita.contenttypes.testing import RESTAPI_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from transaction import commit

import unittest


class TestSerializerSummary(unittest.TestCase):
    """"""

    layer = RESTAPI_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

        self.request["LANGUAGE"] = "it"

        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    def test_summary_serializer_always_return_parliamo_di_metadata(self):
        """ """
        struttura = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Test servizio",
            parliamo_di=["ticket-ed-esenzioni", "igiene-pubblica"],
        )
        commit()

        resp = self.api_session.get(f"@search?UID={struttura.UID()}").json()
        self.assertEqual(resp["items_total"], 1)
        self.assertIn("parliamo_di_metadata", resp["items"][0])
        self.assertEqual(
            resp["items"][0]["parliamo_di_metadata"],
            [
                {"title": "Ticket ed esenzioni", "token": "ticket-ed-esenzioni"},
                {"title": "Igiene Pubblica", "token": "igiene-pubblica"},
            ],
        )

    def test_summary_serializer_always_return_a_chi_si_rivolge_tassonomia_metadata(
        self,
    ):
        """ """
        struttura = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Test servizio",
            a_chi_si_rivolge_tassonomia=[
                "farmacie",
                "imprese",
            ],
        )

        commit()
        resp = self.api_session.get(f"@search?UID={struttura.UID()}").json()

        self.assertEqual(resp["items_total"], 1)
        self.assertIn("a_chi_si_rivolge_tassonomia_metadata", resp["items"][0])
        self.assertEqual(
            resp["items"][0]["a_chi_si_rivolge_tassonomia_metadata"],
            [
                {"title": "Farmacie", "token": "farmacie"},
                {"title": "Imprese", "token": "imprese"},
            ],
        )

    def test_summary_serializer_always_return_id_metadata(
        self,
    ):
        """ """
        struttura = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Test servizio",
            a_chi_si_rivolge_tassonomia=[
                "farmacie",
                "imprese",
            ],
        )

        commit()
        resp = self.api_session.get(f"@search?UID={struttura.UID()}").json()

        self.assertEqual(resp["items_total"], 1)
        self.assertIn("id", resp["items"][0])
        self.assertEqual(
            resp["items"][0]["id"],
            "test-servizio",
        )
