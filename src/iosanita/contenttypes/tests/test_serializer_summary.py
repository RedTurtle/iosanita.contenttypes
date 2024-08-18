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

    def test_summary_serializer_always_return_tipologia_notizia_metadata(
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

        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="Test news",
            tipologia_notizia=["notizia"],
        )

        commit()
        resp = self.api_session.get(f"@search?UID={struttura.UID()}").json()

        self.assertEqual(resp["items_total"], 1)
        self.assertIn("tipologia_notizia", resp["items"][0])
        self.assertEqual(resp["items"][0]["tipologia_notizia"], [])

        resp = self.api_session.get(f"@search?UID={news.UID()}").json()

        self.assertEqual(resp["items_total"], 1)
        self.assertIn("tipologia_notizia", resp["items"][0])
        self.assertEqual(resp["items"][0]["tipologia_notizia"], ["notizia"])

    def test_summary_serializer_return_has_children_info_in_GET_calls(self):
        """ """
        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="Test news",
        )

        api.content.create(
            container=news["video"],
            type="Link",
            title="Test link",
        )
        commit()
        resp = self.api_session.get(news.absolute_url()).json()

        self.assertEqual(len(resp["items"]), 3)
        self.assertIn("has_children", resp["items"][0])
        self.assertIn("has_children", resp["items"][1])
        self.assertIn("has_children", resp["items"][2])
        self.assertFalse(resp["items"][0]["has_children"])
        self.assertTrue(resp["items"][1]["has_children"])
        self.assertFalse(resp["items"][2]["has_children"])

    def test_summary_serializer_does_not_return_has_children_info_in_POST_calls(self):
        """ """
        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="Test news",
        )

        api.content.create(
            container=news["video"],
            type="Link",
            title="Test link",
        )
        commit()
        resp = self.api_session.get(
            f"@search?path={'/'.join(news.getPhysicalPath())}&id=video"
        ).json()

        self.assertEqual(len(resp["items"]), 1)
        self.assertNotIn("has_children", resp["items"][0])

        resp = self.api_session.get(
            f"@search?path={'/'.join(news.getPhysicalPath())}&id=documenti"
        ).json()

        self.assertEqual(len(resp["items"]), 1)
        self.assertNotIn("has_children", resp["items"][0])
