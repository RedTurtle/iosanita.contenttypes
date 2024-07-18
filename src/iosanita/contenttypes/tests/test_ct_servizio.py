# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from iosanita.contenttypes.testing import RESTAPI_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession

import unittest


class TestServizioSchema(unittest.TestCase):
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

    def test_behaviors_enabled_for_servizio(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Servizio"].behaviors,
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
                "iosanita.contenttypes.behavior.contatti",
                "iosanita.contenttypes.behavior.a_chi_si_rivolge",
                "collective.taxonomy.generated.a_chi_si_rivolge_tassonomia",
                "collective.taxonomy.generated.parliamo_di",
                "iosanita.contenttypes.behavior.ulteriori_informazioni",
            ),
        )

    def test_servizio_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(len(resp["fieldsets"]), 18)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "cosa_serve",
                "accedi_al_servizio",
                "tempi_attesa",
                "costi",
                "dove",
                "orari",
                "contatti",
                "cosa_e",
                "a_chi_si_rivolge",
                "procedure_collegate_esito",
                "responsabili",
                "ulteriori_informazioni",
                "settings",
                "ownership",
                "dates",
                "categorization",
                "seo",
            ],
        )

    def test_servizio_required_fields(self):
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "title",
                    "cosa_serve",
                    "come_accedere",
                    "tempi_attesa",
                    "costi",
                    "orari",
                    "uo_correlata",
                    "responsabile_correlato",
                    "punti_di_contatto",
                    "a_chi_si_rivolge",
                    "description",
                ]
            ),
        )

    def test_servizio_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "stato_servizio",
                "sottotitolo",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "parliamo_di",
            ],
        )

    def test_servizio_fields_cosa_serve_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            ["cosa_serve"],
        )

    def test_servizio_fields_accedi_al_servizio_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            ["come_accedere", "piattaforma_online_link", "piattaforma_online_label"],
        )

    def test_servizio_fields_tempi_attesa_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
            ["tempi_attesa"],
        )

    def test_servizio_fields_costi_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            ["costi"],
        )

    def test_servizio_fields_struttura_correlata_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(resp["fieldsets"][5]["fields"], ["struttura_correlata"])

    def test_servizio_fields_orari_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(resp["fieldsets"][6]["fields"], ["orari"])

    def test_servizio_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(resp["fieldsets"][7]["fields"], ["punti_di_contatto"])

    def test_servizio_fields_cosa_e_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(resp["fieldsets"][8]["fields"], ["descrizione_estesa"])

    def test_servizio_fields_a_chi_si_rivolge_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][9]["fields"],
            ["a_chi_si_rivolge", "a_chi_si_rivolge_tassonomia"],
        )

    def test_servizio_fields_esito_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(resp["fieldsets"][10]["fields"], ["procedure_collegate_esito"])

    def test_servizio_fields_responsabili_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(
            resp["fieldsets"][11]["fields"],
            ["uo_correlata", "responsabile_correlato"],
        )

    def test_servizio_fields_ulteriori_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Servizio").json()
        self.assertEqual(resp["fieldsets"][12]["fields"], ["ulteriori_informazioni"])