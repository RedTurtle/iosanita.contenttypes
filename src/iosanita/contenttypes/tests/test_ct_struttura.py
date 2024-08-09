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


class TestStrutturaSchema(unittest.TestCase):
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

    def test_behaviors_enabled_for_struttura(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Struttura"].behaviors,
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
                "plone.constraintypes",
                "plone.leadimage",
                "volto.preview_image",
                "plone.relateditems",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "iosanita.contenttypes.behavior.dove_struttura",
                "iosanita.contenttypes.behavior.ulteriori_informazioni",
                "iosanita.contenttypes.behavior.a_chi_si_rivolge",
                "collective.taxonomy.generated.a_chi_si_rivolge_tassonomia",
                "iosanita.contenttypes.behavior.contatti",
                "collective.taxonomy.generated.parliamo_di",
            ),
        )

    def test_struttura_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(len(resp["fieldsets"]), 16)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "cosa_e",
                "a_chi_si_rivolge",
                "dove",
                "come_accedere",
                "orari",
                "contatti",
                "servizi",
                "persone_struttura",
                "contenuti_collegati",
                "ulteriori_informazioni",
                "seo",
                "settings",
                "ownership",
                "dates",
                "categorization",
            ],
        )

    def test_struttura_required_fields(self):
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "come_accedere",
                    # "description", is required from schema_tweaks.py but it doesn't apply in test
                    "orari",
                    "pdc_correlato",
                    "responsabile_correlato",
                    "title",
                ]
            ),
        )

    def test_struttura_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
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
                "parliamo_di",
            ],
        )

    def test_struttura_fields_cosa_e_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            ["descrizione_estesa"],
        )

    def test_struttura_fields_a_chi_si_rivolge_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            ["a_chi_si_rivolge", "a_chi_si_rivolge_tassonomia"],
        )

    def test_struttura_fields_dove_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            [
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

    def test_struttura_fields_come_accedere_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            ["come_accedere"],
        )

    def test_struttura_fields_orari_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(resp["fieldsets"][5]["fields"], ["orari"])

    def test_struttura_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(resp["fieldsets"][6]["fields"], ["pdc_correlato"])

    def test_struttura_fields_servizi_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(resp["fieldsets"][7]["fields"], ["servizi"])

    def test_struttura_fields_persone_struttura_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(
            resp["fieldsets"][8]["fields"],
            ["responsabile_correlato", "coordinatore_correlato"],
        )

    def test_struttura_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(
            resp["fieldsets"][9]["fields"],
            ["uo_correlata", "struttura_correlata"],
        )

    def test_struttura_fields_ulteriori_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(
            resp["fieldsets"][10]["fields"],
            ["ulteriori_informazioni"],
        )


class TestStruttura(unittest.TestCase):
    """"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_struttura_default_children(self):
        struttura = api.content.create(
            container=self.portal, type="Struttura", title="xxx"
        )

        self.assertEqual(struttura.keys(), ["documenti", "multimedia"])
