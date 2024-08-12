# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from iosanita.contenttypes.testing import INTEGRATION_TESTING
from iosanita.contenttypes.testing import RESTAPI_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.testing import RelativeSession
from zope.component import queryMultiAdapter
from iosanita.contenttypes.interfaces import IoSanitaMigrationMarker
from zope.interface import alsoProvides

import unittest


class TestNewsSchema(unittest.TestCase):
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

    def test_behaviors_enabled_for_bando(self):
        portal_types = api.portal.get_tool(name="portal_types")
        self.assertEqual(
            portal_types["News Item"].behaviors,
            (
                "plone.dublincore",
                "plone.namefromtitle",
                "plone.allowdiscussion",
                "plone.shortname",
                "plone.excludefromnavigation",
                "plone.relateditems",
                "plone.leadimage",
                "plone.versioning",
                "plone.locking",
                "volto.preview_image",
                "plone.constraintypes",
                "plone.textindexer",
                "plone.translatable",
                "kitconcept.seo",
                "collective.taxonomy.generated.tipologia_notizia",
                "collective.taxonomy.generated.parliamo_di",
                "iosanita.contenttypes.behavior.news",
            ),
        )

    def test_bando_fieldsets(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/News Item").json()
        self.assertEqual(len(resp["fieldsets"]), 7)
        self.assertEqual(
            [x.get("id") for x in resp["fieldsets"]],
            [
                "default",
                "correlati",
                "dates",
                "categorization",
                "ownership",
                "settings",
                "seo",
            ],
        )

    def test_bando_required_fields(self):
        resp = self.api_session.get("@types/News Item").json()
        self.assertEqual(
            sorted(resp["required"]),
            sorted(
                [
                    "descrizione_estesa",
                    "title",
                    "uo_correlata",
                    # "description", is required from schema_tweaks.py but it doesn't apply in test
                ]
            ),
        )

    def test_bando_fields_default_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/News Item").json()
        self.assertEqual(
            resp["fieldsets"][0]["fields"],
            [
                "title",
                "description",
                "numero_progressivo_cs",
                "descrizione_estesa",
                "image",
                "image_caption",
                "preview_image",
                "preview_caption",
                "tipologia_notizia",
                "parliamo_di",
            ],
        )

    def test_bando_fields_correlati_fieldset(self):
        """
        Get the list from restapi
        """
        resp = self.api_session.get("@types/News Item").json()
        self.assertEqual(
            resp["fieldsets"][1]["fields"],
            [
                "persona_correlata",
                "struttura_correlata",
                "servizio_correlato",
                "uo_correlata",
                "notizia_correlata",
            ],
        )


class TestNews(unittest.TestCase):
    """"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.request["LANGUAGE"] = "it"

        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_news_default_children(self):
        news = api.content.create(container=self.portal, type="News Item", title="xxx")

        self.assertEqual(news.keys(), ["multimedia", "documenti-allegati"])

        self.assertEqual("Document", news["multimedia"].portal_type)
        self.assertEqual("Document", news["documenti-allegati"].portal_type)

    def test_news_default_children_disabled_with_marker_interface(self):
        alsoProvides(self.request, IoSanitaMigrationMarker)
        uo = api.content.create(container=self.portal, type="News Item", title="xxx")

        self.assertEqual(len(uo.keys()), 0)

    def test_news_type_title_based_on_tipologia_notizia(self):
        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="xxx",
            tipologia_notizia="notizia",
        )

        serializer = queryMultiAdapter((news, self.request), ISerializeToJson)()

        self.assertEqual(serializer["type_title"], "Notizia")

        news.tipologia_notizia = "comunicato-stampa"

        serializer = queryMultiAdapter((news, self.request), ISerializeToJson)()

        self.assertEqual(serializer["type_title"], "Comunicato (stampa)")

    def test_news_type_title_based_on_tipologia_notizia_on_brains(self):
        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="xxx",
            tipologia_notizia="notizia",
        )

        brain = api.content.find(UID=news.UID())[0]
        serializer = queryMultiAdapter((brain, self.request), ISerializeToJsonSummary)()

        self.assertEqual(serializer["type_title"], "Notizia")

        news.tipologia_notizia = "comunicato-stampa"
        news.reindexObject()

        brain = api.content.find(UID=news.UID())[0]
        serializer = queryMultiAdapter((brain, self.request), ISerializeToJsonSummary)()

        self.assertEqual(serializer["type_title"], "Comunicato (stampa)")

    def test_news_type_title_default_if_wrong_tipologia_notizia(self):
        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="xxx",
            tipologia_notizia="xxx",
        )

        serializer = queryMultiAdapter((news, self.request), ISerializeToJson)()

        self.assertEqual(serializer["type_title"], "Notizia")

    def test_news_type_title_default_if_wrong_tipologia_notizia_on_brains(self):
        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="xxx",
            tipologia_notizia="xxx",
        )

        brain = api.content.find(UID=news.UID())[0]
        serializer = queryMultiAdapter((brain, self.request), ISerializeToJsonSummary)()

        self.assertEqual(serializer["type_title"], "Notizia")
