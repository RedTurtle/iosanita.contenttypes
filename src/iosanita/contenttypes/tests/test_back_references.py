# -*- coding: utf-8 -*-
"""Setup tests for this package."""
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
from plone.restapi.interfaces import ISerializeToJsonSummary
from zope.component import getMultiAdapter
from transaction import commit

import unittest


class TestBackReferences(unittest.TestCase):
    """"""

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

    def test_servizio_expander(self):
        servizio = api.content.create(
            container=self.portal, type="Servizio", title="Servizio"
        )
        commit()
        resp = self.api_session.get(
            f"{servizio.absolute_url()}?expand=back-references"
        ).json()["@components"]

        self.assertIn("back-references", resp)
        self.assertEqual(
            ["@id", "documenti", "news"], list(resp["back-references"].keys())
        )

    def test_servizio_expander_return_related_news(self):
        servizio = api.content.create(
            container=self.portal, type="Servizio", title="Servizio"
        )
        intids = getUtility(IIntIds)
        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="News",
            servizio_correlato=[RelationValue(intids.getId(servizio))],
        )

        commit()

        resp = self.api_session.get(
            f"{servizio.absolute_url()}?expand=back-references"
        ).json()["@components"]["back-references"]

        self.assertEqual(len(resp["news"]), 1)
        self.assertEqual(len(resp["documenti"]), 0)
        self.assertEqual(
            resp["news"][0],
            getMultiAdapter(
                (api.content.find(UID=news.UID())[0], self.request),
                ISerializeToJsonSummary,
            )(),
        )

    def test_servizio_expander_return_related_news_sorted_by_effective_date(self):
        servizio = api.content.create(
            container=self.portal, type="Servizio", title="Servizio"
        )
        intids = getUtility(IIntIds)
        news1 = api.content.create(
            container=self.portal,
            type="News Item",
            title="News",
            servizio_correlato=[RelationValue(intids.getId(servizio))],
        )
        news2 = api.content.create(
            container=self.portal,
            type="News Item",
            title="News",
            servizio_correlato=[RelationValue(intids.getId(servizio))],
        )
        news3 = api.content.create(
            container=self.portal,
            type="News Item",
            title="News",
            servizio_correlato=[RelationValue(intids.getId(servizio))],
        )

        api.content.transition(obj=news2, transition="publish")
        api.content.transition(obj=news3, transition="publish")
        api.content.transition(obj=news1, transition="publish")

        news2.setEffectiveDate(news2.effective() + 1)
        news3.setEffectiveDate(news3.effective() + 2)
        news1.setEffectiveDate(news1.effective() + 3)

        news1.reindexObject()
        news2.reindexObject()
        news3.reindexObject()

        commit()

        resp = self.api_session.get(
            f"{servizio.absolute_url()}?expand=back-references"
        ).json()["@components"]["back-references"]

        self.assertEqual(len(resp["news"]), 3)
        self.assertEqual(
            resp["news"][0],
            getMultiAdapter(
                (api.content.find(UID=news1.UID())[0], self.request),
                ISerializeToJsonSummary,
            )(),
        )
        self.assertEqual(
            resp["news"][1],
            getMultiAdapter(
                (api.content.find(UID=news3.UID())[0], self.request),
                ISerializeToJsonSummary,
            )(),
        )

    def test_servizio_expander_return_related_documenti(self):
        servizio = api.content.create(
            container=self.portal, type="Servizio", title="Servizio"
        )
        intids = getUtility(IIntIds)
        documento = api.content.create(
            container=self.portal,
            type="Documento",
            title="documento",
            servizio_procedura_riferimento=[RelationValue(intids.getId(servizio))],
        )

        commit()

        resp = self.api_session.get(
            f"{servizio.absolute_url()}?expand=back-references"
        ).json()["@components"]["back-references"]

        self.assertEqual(len(resp["documenti"]), 1)
        self.assertEqual(len(resp["news"]), 0)
        self.assertEqual(
            resp["documenti"][0]["@id"],
            documento.absolute_url(),
        )

    def test_struttura_expander(self):
        struttura = api.content.create(
            container=self.portal, type="Struttura", title="Struttura"
        )
        commit()
        resp = self.api_session.get(
            f"{struttura.absolute_url()}?expand=back-references"
        ).json()["@components"]

        self.assertIn("back-references", resp)
        self.assertEqual(["@id", "news"], list(resp["back-references"].keys()))

    def test_struttura_expander_return_related_news(self):
        struttura = api.content.create(
            container=self.portal, type="Struttura", title="Struttura"
        )
        intids = getUtility(IIntIds)
        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="News",
            struttura_correlata=[RelationValue(intids.getId(struttura))],
        )

        commit()

        resp = self.api_session.get(
            f"{struttura.absolute_url()}?expand=back-references"
        ).json()["@components"]["back-references"]

        self.assertEqual(len(resp["news"]), 1)
        self.assertEqual(
            resp["news"][0],
            getMultiAdapter(
                (api.content.find(UID=news.UID())[0], self.request),
                ISerializeToJsonSummary,
            )(),
        )

    def test_uo_expander(self):
        uo = api.content.create(
            container=self.portal, type="UnitaOrganizzativa", title="UO"
        )
        commit()
        resp = self.api_session.get(
            f"{uo.absolute_url()}?expand=back-references"
        ).json()["@components"]

        self.assertIn("back-references", resp)
        self.assertEqual(["@id", "news"], list(resp["back-references"].keys()))

    def test_uo_expander_return_related_news(self):
        uo = api.content.create(
            container=self.portal, type="UnitaOrganizzativa", title="UO"
        )
        intids = getUtility(IIntIds)
        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="News",
            uo_correlata=[RelationValue(intids.getId(uo))],
        )

        commit()

        resp = self.api_session.get(
            f"{uo.absolute_url()}?expand=back-references"
        ).json()["@components"]["back-references"]

        self.assertEqual(len(resp["news"]), 1)
        self.assertEqual(
            resp["news"][0],
            getMultiAdapter(
                (api.content.find(UID=news.UID())[0], self.request),
                ISerializeToJsonSummary,
            )(),
        )

    def test_persona_expander(self):
        persona = api.content.create(
            container=self.portal, type="Persona", title="persona"
        )
        commit()
        resp = self.api_session.get(
            f"{persona.absolute_url()}?expand=back-references"
        ).json()["@components"]

        self.assertIn("back-references", resp)
        self.assertEqual(
            ["@id", "personale", "responsabile"], list(resp["back-references"].keys())
        )

    def test_persona_expander_return_related_news(self):
        persona = api.content.create(
            container=self.portal, type="Persona", title="persona"
        )
        intids = getUtility(IIntIds)
        uo1 = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="UO1",
            responsabile_correlato=[RelationValue(intids.getId(persona))],
        )
        uo2 = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="bbb UO2",
            personale_correlato=[RelationValue(intids.getId(persona))],
        )
        uo3 = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="ccc UO2",
            personale_correlato=[RelationValue(intids.getId(persona))],
        )
        uo4 = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="aaa UO2",
            personale_correlato=[RelationValue(intids.getId(persona))],
        )

        commit()

        resp = self.api_session.get(
            f"{persona.absolute_url()}?expand=back-references"
        ).json()["@components"]["back-references"]
        self.assertEqual(len(resp["responsabile"]), 1)
        self.assertEqual(resp["responsabile"][0]["@id"], uo1.absolute_url())

        # references are in alphabetical order exept news (that are ordered by date)
        self.assertEqual(len(resp["personale"]), 3)
        self.assertEqual(resp["personale"][0]["@id"], uo4.absolute_url())
        self.assertEqual(resp["personale"][1]["@id"], uo2.absolute_url())
        self.assertEqual(resp["personale"][2]["@id"], uo3.absolute_url())
