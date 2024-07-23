# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from iosanita.contenttypes.testing import RESTAPI_TESTING, INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession

import unittest


class TestEventSchema(unittest.TestCase):
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

    def test_behaviors_enabled_for_event(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["Event"].behaviors,
            (
                "plone.textindexer",
                "plone.eventbasic",
                "plone.eventrecurrence",
                "plone.dublincore",
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.excludefromnavigation",
                "plone.shortname",
                "plone.relateditems",
                "plone.versioning",
                "plone.locking",
                "plone.constraintypes",
                "volto.preview_image",
                "plone.translatable",
                "kitconcept.seo",
                "iosanita.contenttypes.behavior.a_chi_si_rivolge",
                "collective.taxonomy.generated.a_chi_si_rivolge_tassonomia",
                "iosanita.contenttypes.behavior.ulteriori_informazioni",
                "iosanita.contenttypes.behavior.evento",
                "iosanita.contenttypes.behavior.dove",
                "iosanita.contenttypes.behavior.contatti",
                "iosanita.contenttypes.behavior.ulteriori_informazioni",
                "collective.taxonomy.generated.tipologia_evento",
                "collective.taxonomy.generated.parliamo_di",
            ),
        )

    def test_event_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(len(resp["fieldsets"]), 14)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "cosa_e",
                "partecipanti",
                "dove",
                "costi",
                "contatti",
                "ulteriori_informazioni",
                "a_chi_si_rivolge",
                "contenuti_collegati",
                "categorization",
                "dates",
                "ownership",
                "settings",
                "seo",
            ],
        )

    def test_event_required_fields(self):
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "title",
                    "start",
                    "end",
                    "tipologia_evento",
                    "a_chi_si_rivolge",
                    "descrizione_estesa",
                    "costo",
                    "punti_di_contatto",
                    # "description", is required from schema_tweaks.py but it doesn't apply in test
                ]
            ),
        )

    def test_event_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "start",
                "end",
                "whole_day",
                "open_end",
                "sync_uid",
                "recurrence",
                "preview_image",
                "preview_caption",
                "tipologia_evento",
                "parliamo_di",
            ],
        )

    def test_event_fields_cosa_e_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(resp["fieldsets"][1]["fields"], ["descrizione_estesa"])

    def test_event_fields_partecipanti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][2]["fields"],
            ["persona_correlata", "parteciperanno"],
        )

    def test_event_fields_dove_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][3]["fields"],
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

    def test_event_fields_costi_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            ["costo"],
        )

    def test_event_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][5]["fields"],
            [
                "organizzato_da_interno",
                "organizzato_da_esterno",
                "patrocinato_da",
                "punti_di_contatto",
            ],
        )

    def test_event_fields_ulteriori_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(resp["fieldsets"][6]["fields"], ["ulteriori_informazioni"])

    def test_event_fields_a_chi_si_rivolge_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(
            resp["fieldsets"][7]["fields"],
            ["a_chi_si_rivolge", "a_chi_si_rivolge_tassonomia"],
        )

    def test_event_fields_contenuti_collegati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Event").json()
        self.assertEqual(resp["fieldsets"][8]["fields"], ["eventi_correlati"])


class TestEvent(unittest.TestCase):
    """"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_if_event_has_children_events_is_indexed_as_rassegna(self):
        parent = api.content.create(container=self.portal, type="Event", title="parent")

        brain = api.content.find(UID=parent.UID())[0]

        self.assertFalse(brain.rassegna)

        api.content.create(container=parent, type="Event", title="child")

        brain = api.content.find(UID=parent.UID())[0]

        self.assertTrue(brain.rassegna)

    def test_event_default_children(self):
        event = api.content.create(container=self.portal, type="Event", title="xxx")

        self.assertEqual(
            event.keys(), ["immagini", "video", "sponsor-evento", "documenti"]
        )
