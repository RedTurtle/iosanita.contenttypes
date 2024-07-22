# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from iosanita.contenttypes.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestTaxonomiesCustomMetadata(unittest.TestCase):
    """"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

        self.request["LANGUAGE"] = "it"

        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_parliamo_di_metadata_has_array_of_objects(self):
        """ """
        struttura = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Test servizio",
            parliamo_di=["ticket-ed-esenzioni", "igiene-pubblica"],
        )
        res = api.content.find(UID=struttura.UID())

        self.assertEqual(len(res), 1)
        self.assertEqual(
            res[0].parliamo_di, sorted(["ticket-ed-esenzioni", "igiene-pubblica"])
        )
        self.assertEqual(
            res[0].parliamo_di_metadata,
            [
                {"title": "Ticket ed esenzioni", "token": "ticket-ed-esenzioni"},
                {"title": "Igiene Pubblica", "token": "igiene-pubblica"},
            ],
        )

    def test_a_chi_si_rivolge_tassonomia_metadata_has_array_of_objects(self):
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
        res = api.content.find(UID=struttura.UID())

        self.assertEqual(len(res), 1)
        self.assertEqual(
            res[0].a_chi_si_rivolge_tassonomia,
            sorted(["farmacie", "imprese"]),
        )
        self.assertEqual(
            res[0].a_chi_si_rivolge_tassonomia_metadata,
            [
                {"title": "Farmacie", "token": "farmacie"},
                {"title": "Imprese", "token": "imprese"},
            ],
        )
