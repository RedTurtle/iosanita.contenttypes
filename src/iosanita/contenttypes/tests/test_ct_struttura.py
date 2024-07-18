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
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.event import notify
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent

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
                "iosanita.contenttypes.behavior.dove",
                "iosanita.contenttypes.behavior.ulteriori_informazioni",
                "iosanita.contenttypes.behavior.a_chi_si_rivolge",
                "collective.taxonomy.generated.a_chi_si_rivolge_tassonomia",
                "iosanita.contenttypes.behavior.contatti",
                "iosanita.contenttypes.behavior.servizi",
                "collective.taxonomy.generated.parliamo_di",
                "iosanita.contenttypes.behavior.strutture_correlate",
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
                "orari_apertura",
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
                    "a_chi_si_rivolge",
                    "come_accedere",
                    "orari_apertura",
                    "punti_di_contatto",
                    "responsabile_struttura",
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

    def test_struttura_fields_come_accedere_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(
            resp["fieldsets"][4]["fields"],
            ["come_accedere"],
        )

    def test_struttura_fields_orari_apertura_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(resp["fieldsets"][5]["fields"], ["orari_apertura"])

    def test_struttura_fields_contatti_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(resp["fieldsets"][6]["fields"], ["punti_di_contatto"])

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
            ["responsabile_struttura", "coordinatore_struttura", "personale_struttura"],
        )

    def test_struttura_fields_contenuti_collegati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(
            resp["fieldsets"][9]["fields"],
            ["uo_appartenenza", "strutture_correlate"],
        )

    def test_struttura_fields_ulteriori_informazioni_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/Struttura").json()
        self.assertEqual(resp["fieldsets"][10]["fields"], ["ulteriori_informazioni"])


class TestStruttura(unittest.TestCase):
    """Test that design.plone.contenttypes is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.uo = api.content.create(
            container=self.portal, type="UnitaOrganizzativa", title="uo"
        )

    def test_uo_appartenenza_reference_is_in_catalog(self):
        """ """
        struttura = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Test servizio",
        )
        intids = getUtility(IIntIds)
        struttura.uo_appartenenza = [RelationValue(intids.getId(self.uo))]
        notify(ObjectModifiedEvent(struttura))

        res = api.content.find(uo_appartenenza_uid=self.uo.UID())

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].UID, struttura.UID())
