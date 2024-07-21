# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from iosanita.contenttypes.testing import RESTAPI_TESTING, INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from plone.dexterity.utils import createContentInContainer

import unittest


class TestPersonaSchema(unittest.TestCase):
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

    def test_behaviors_enabled_for_persona(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Persona"].behaviors,
            (
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.ownership",
                "plone.publication",
                "plone.relateditems",
                "plone.categorization",
                "plone.locking",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "plone.versioning",
                "plone.constraintypes",
                "collective.taxonomy.generated.incarico",
                "iosanita.contenttypes.behavior.dove",
                "iosanita.contenttypes.behavior.contatti",
                "iosanita.contenttypes.behavior.ulteriori_informazioni",
            ),
        )

    def test_persona_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(len(resp["fieldsets"]), 13)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "incarichi",
                "competenze",
                "dove",
                "orari_ricevimento",
                "contatti",
                "biografia",
                "ulteriori_informazioni",
                "settings",
                "ownership",
                "dates",
                "categorization",
                "seo",
            ],
        )

    def test_persona_required_fields(self):
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "cognome",
                    "competenze",
                    "description",
                    "incarico",
                    "nome",
                    "punti_di_contatto",
                ]
            ),
        )

    def test_persona_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "cognome",
                "nome",
                "titolo_persona",
                "description",
                "image",
                "uo_correlata",
                "struttura_correlata",
            ],
        )

    def test_persona_fields_incarichi_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"], ["incarico", "altri_incarichi"]
        )

    def test_persona_fields_competenze_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            ["competenze"],
        )

    def test_persona_fields_dove_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            [
                "struttura_ricevimento",
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

    def test_persona_fields_orari_ricevimento_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            ["orari_ricevimento"],
        )

    def test_persona_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(resp["fieldsets"][5]["fields"], ["punti_di_contatto"])

    def test_persona_fields_biografia_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(resp["fieldsets"][6]["fields"], ["biografia"])

    def test_persona_fields_ulteriori_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Persona").json()
        self.assertEqual(resp["fieldsets"][7]["fields"], ["ulteriori_informazioni"])


class TestPersona(unittest.TestCase):
    """"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_persona_title_composed(self):
        createContentInContainer(self.portal, "Persona", nome="John", cognome="Doe")
        self.assertIn("doe-john", self.portal.keys())
        persona = self.portal["doe-john"]
        self.assertEqual(persona.title, "Doe John")

    def test_persona_title_composed_also_with_titolo(self):
        createContentInContainer(
            self.portal, "Persona", nome="John", cognome="Doe", titolo_persona="dr."
        )
        self.assertIn("dr-doe-john", self.portal.keys())
        persona = self.portal["dr-doe-john"]
        self.assertEqual(persona.title, "dr. Doe John")
