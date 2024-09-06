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
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

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

    def test_expander_called_on_generic_content_does_not_return_anything(self):
        link = api.content.create(container=self.portal, type="Link", title="Link")
        commit()
        resp = self.api_session.get(f"{link.absolute_url()}/@back-references").json()

        self.assertEqual(["@id"], list(resp.keys()))

    def test_expander_on_registered_ct_return_nothing_if_no_relations_are_set(self):
        servizio = api.content.create(
            container=self.portal, type="Servizio", title="Servizio"
        )
        commit()
        resp = self.api_session.get(
            f"{servizio.absolute_url()}/@back-references"
        ).json()

        self.assertEqual(["@id"], list(resp.keys()))

    def test_expander_return_related_news_sorted_by_Date(self):
        """
        Date metadata is modifified date for contents not yet published, or
        effective date for published contents
        """
        servizio = api.content.create(
            container=self.portal, type="Servizio", title="Servizio"
        )
        intids = getUtility(IIntIds)
        news1 = api.content.create(
            container=self.portal,
            type="News Item",
            title="News 1",
            servizio_correlato=[RelationValue(intids.getId(servizio))],
        )
        news2 = api.content.create(
            container=self.portal,
            type="News Item",
            title="News 2",
            servizio_correlato=[RelationValue(intids.getId(servizio))],
        )
        news3 = api.content.create(
            container=self.portal,
            type="News Item",
            title="News 3",
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
            f"{servizio.absolute_url()}/@back-references"
        ).json()

        self.assertEqual(len(resp["News Item"]), 3)
        self.assertEqual(resp["News Item"][0]["@id"], news1.absolute_url())
        self.assertEqual(resp["News Item"][1]["@id"], news3.absolute_url())
        self.assertEqual(resp["News Item"][2]["@id"], news2.absolute_url())

    # SERVIZIO

    def test_servizio_expander_return_related_contents_splitted_by_portal_type(self):
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

        servizio2 = api.content.create(
            container=self.portal,
            type="Servizio",
            title="servizio 2",
            servizio_correlato=[RelationValue(intids.getId(servizio))],
        )

        commit()

        resp = self.api_session.get(
            f"{servizio.absolute_url()}/@back-references"
        ).json()

        self.assertEqual(["@id", "Documento", "Servizio"], list(resp.keys()))
        self.assertEqual(len(resp["Documento"]), 1)
        self.assertEqual(len(resp["Servizio"]), 1)
        self.assertEqual(
            resp["Documento"][0]["@id"],
            documento.absolute_url(),
        )
        self.assertEqual(
            resp["Servizio"][0]["@id"],
            servizio2.absolute_url(),
        )

    def test_struttura_expander_return_related_contents_splitted_by_portal_type(self):
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
        event = api.content.create(
            container=self.portal,
            type="Event",
            title="Event",
            struttura_correlata=[RelationValue(intids.getId(struttura))],
        )
        service = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Servizio",
            struttura_correlata=[RelationValue(intids.getId(struttura))],
        )
        uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="uo",
            struttura_correlata=[RelationValue(intids.getId(struttura))],
        )

        commit()

        resp = self.api_session.get(
            f"{struttura.absolute_url()}/@back-references"
        ).json()

        self.assertEqual(
            list(resp.keys()),
            ["@id", "Event", "News Item", "Servizio", "UnitaOrganizzativa"],
        )

        self.assertEqual(len(resp["Event"]), 1)
        self.assertEqual(len(resp["News Item"]), 1)
        self.assertEqual(len(resp["Servizio"]), 1)
        self.assertEqual(len(resp["UnitaOrganizzativa"]), 1)

        self.assertEqual(resp["Event"][0]["@id"], event.absolute_url())
        self.assertEqual(resp["News Item"][0]["@id"], news.absolute_url())
        self.assertEqual(resp["Servizio"][0]["@id"], service.absolute_url())
        self.assertEqual(resp["UnitaOrganizzativa"][0]["@id"], uo.absolute_url())

    def test_uo_expander_return_related_contents_splitted_by_portal_type(self):
        uo = api.content.create(
            container=self.portal, type="UnitaOrganizzativa", title="uo"
        )
        intids = getUtility(IIntIds)

        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="News",
            uo_correlata=[RelationValue(intids.getId(uo))],
        )
        documento = api.content.create(
            container=self.portal,
            type="Documento",
            title="Documento",
            uo_correlata=[RelationValue(intids.getId(uo))],
        )
        pdc = api.content.create(
            container=self.portal,
            type="PuntoDiContatto",
            title="pdc",
            uo_correlata=[RelationValue(intids.getId(uo))],
        )
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Servizio",
            uo_correlata=[RelationValue(intids.getId(uo))],
        )
        struttura = api.content.create(
            container=self.portal,
            type="Struttura",
            title="struttura",
            uo_correlata=[RelationValue(intids.getId(uo))],
        )

        commit()

        resp = self.api_session.get(f"{uo.absolute_url()}/@back-references").json()

        self.assertEqual(
            list(resp.keys()),
            [
                "@id",
                "Documento",
                "News Item",
                "PuntoDiContatto",
                "Servizio",
                "Struttura",
            ],
        )

        self.assertEqual(len(resp["Documento"]), 1)
        self.assertEqual(len(resp["News Item"]), 1)
        self.assertEqual(len(resp["PuntoDiContatto"]), 1)
        self.assertEqual(len(resp["Servizio"]), 1)
        self.assertEqual(len(resp["Struttura"]), 1)

        self.assertEqual(resp["Documento"][0]["@id"], documento.absolute_url())
        self.assertEqual(resp["News Item"][0]["@id"], news.absolute_url())
        self.assertEqual(resp["Servizio"][0]["@id"], servizio.absolute_url())
        self.assertEqual(resp["PuntoDiContatto"][0]["@id"], pdc.absolute_url())
        self.assertEqual(resp["Struttura"][0]["@id"], struttura.absolute_url())

    def test_persona_expander_return_related_contents_splitted_by_portal_type(self):
        persona = api.content.create(
            container=self.portal, type="Persona", title="persona"
        )
        intids = getUtility(IIntIds)

        news = api.content.create(
            container=self.portal,
            type="News Item",
            title="News",
            persona_correlata=[RelationValue(intids.getId(persona))],
        )
        evento = api.content.create(
            container=self.portal,
            type="Event",
            title="event",
            persona_correlata=[RelationValue(intids.getId(persona))],
        )

        commit()

        resp = self.api_session.get(f"{persona.absolute_url()}/@back-references").json()

        self.assertEqual(
            list(resp.keys()),
            ["@id", "Event", "News Item", "personale", "responsabile"],
        )

        self.assertEqual(len(resp["News Item"]), 1)
        self.assertEqual(len(resp["Event"]), 1)

        self.assertEqual(resp["News Item"][0]["@id"], news.absolute_url())
        self.assertEqual(resp["Event"][0]["@id"], evento.absolute_url())

    def test_persona_expander_return_responsabile_and_personale_splitted_by_type(self):
        persona = api.content.create(
            container=self.portal, type="Persona", title="persona"
        )
        intids = getUtility(IIntIds)

        uo = api.content.create(
            container=self.portal,
            type="UnitaOrganizzativa",
            title="uo",
            responsabile_correlato=[RelationValue(intids.getId(persona))],
            personale_correlato=[RelationValue(intids.getId(persona))],
        )
        servizio = api.content.create(
            container=self.portal,
            type="Servizio",
            title="Servizio",
            responsabile_correlato=[RelationValue(intids.getId(persona))],
        )
        struttura = api.content.create(
            container=self.portal,
            type="Struttura",
            title="struttura",
            responsabile_correlato=[RelationValue(intids.getId(persona))],
        )

        commit()

        resp = self.api_session.get(f"{persona.absolute_url()}/@back-references").json()

        self.assertEqual(
            list(resp.keys()),
            [
                "@id",
                "personale",
                "responsabile",
            ],
        )

        responsabile = resp["responsabile"]
        personale = resp["personale"]

        self.assertEqual(
            list(responsabile.keys()),
            ["Servizio", "Struttura", "UnitaOrganizzativa"],
        )
        self.assertEqual(
            list(personale.keys()),
            ["UnitaOrganizzativa"],
        )

        self.assertEqual(len(responsabile["UnitaOrganizzativa"]), 1)
        self.assertEqual(len(responsabile["Servizio"]), 1)
        self.assertEqual(len(responsabile["Struttura"]), 1)
        self.assertEqual(responsabile["Servizio"][0]["@id"], servizio.absolute_url())
        self.assertEqual(
            responsabile["UnitaOrganizzativa"][0]["@id"], uo.absolute_url()
        )
        self.assertEqual(responsabile["Struttura"][0]["@id"], struttura.absolute_url())

        self.assertEqual(len(personale["UnitaOrganizzativa"]), 1)
        self.assertEqual(personale["UnitaOrganizzativa"][0]["@id"], uo.absolute_url())
