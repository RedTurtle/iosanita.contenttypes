# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from iosanita.contenttypes.testing import INTEGRATION_TESTING
from iosanita.contenttypes.testing import RESTAPI_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession

import unittest


class TestUOSchema(unittest.TestCase):
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

    def tearDown(self):
        self.api_session.close()

    def test_behaviors_enabled_for_uo(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["UnitaOrganizzativa"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.ownership",
                "plone.publication",
                "plone.categorization",
                "plone.basic",
                "iosanita.contenttypes.behavior.sottotitolo",
                "plone.locking",
                "plone.leadimage",
                "volto.preview_image",
                "plone.relateditems",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "iosanita.contenttypes.behavior.dove",
                "iosanita.contenttypes.behavior.servizi",
                "iosanita.contenttypes.behavior.contatti",
                "iosanita.contenttypes.behavior.ulteriori_informazioni",
            ),
        )

    def test_uo_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(len(resp["fieldsets"]), 14)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "cosa_fa",
                "persone_uo",
                "servizi",
                "dove",
                "orari",
                "contatti",
                "documenti",
                "ulteriori_informazioni",
                "settings",
                "ownership",
                "dates",
                "categorization",
                "seo",
            ],
        )

    def test_uo_required_fields(self):
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "competenze",
                    # "description", is required from schema_tweaks.py but it doesn't apply in test
                    "orari",
                    "punti_di_contatto",
                    "responsabile_correlato",
                    "title",
                ]
            ),
        )

    def test_uo_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "sottotitolo",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
            ],
        )

    def test_uo_fields_cosa_fa_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            ["competenze"],
        )

    def test_uo_fields_persone_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            ["responsabile_correlato", "personale_correlato"],
        )

    def test_uo_fields_servizi_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            ["servizi"],
        )

    def test_uo_fields_dove_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            [
                "luogo_correlato",
                "nome_sede",
                "street",
                "zip_code",
                "city",
                "quartiere",
                "circoscrizione",
                "country",
                "geolocation",
            ],
        )

    def test_uo_fields_orari_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(resp["fieldsets"][5]["fields"], ["orari"])

    def test_uo_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(resp["fieldsets"][6]["fields"], ["punti_di_contatto"])

    def test_uo_fields_documenti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(
            resp["fieldsets"][7]["fields"],
            ["documenti"],
        )

    def test_uo_fields_ulteriori_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/UnitaOrganizzativa").json()
        self.assertEqual(resp["fieldsets"][8]["fields"], ["ulteriori_informazioni"])


class TestUO(unittest.TestCase):
    """"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_uo_default_children(self):
        uo = api.content.create(
            container=self.portal, type="UnitaOrganizzativa", title="xxx"
        )

        self.assertEqual(uo.keys(), ["allegati"])
