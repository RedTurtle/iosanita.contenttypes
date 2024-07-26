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
from transaction import commit

import unittest


class TestCustomValidation(unittest.TestCase):
    layer = RESTAPI_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.request["LANGUAGE"] = "it"

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    def tearDown(self):
        self.api_session.close()

    def test_event_raise_badrequest_if_missing_organizzato_da(self):

        pdc = api.content.create(
            type="PuntoDiContatto", title="pdc", container=self.portal
        )
        commit()
        data = {
            "costo": {"blocks": {}},
            "description": "asdasd",
            "descrizione_estesa": {"blocks": {}},
            "end": "2024-07-26T10:00:00+00:00",
            "geolocation": {"latitude": 44.821502405601, "longitude": 11.632933286779},
            "punti_di_contatto": [{"@id": "/pdc"}],
            "start": "2024-07-26T09:00:00+00:00",
            "tipologia_evento": "giornata-informativa",
            "title": "titolo",
            "@type": "Event",
            "a_chi_si_rivolge": {
                "blocks": {
                    "b8850749-4d5f-4b5f-b842-c050bcf7fd6f": {
                        "@type": "slate",
                        "text": "xxx",
                    }
                },
            },
        }
        resp = self.api_session.post(self.portal_url, json=data)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json()["message"],
            "[{'field': 'organizzato_da_esterno', 'message': \"Devi compilare almeno uno dei due campi per l'organizzazione.\"}, {'field': 'organizzato_da_interno', 'message': \"Devi compilare almeno uno dei due campi per l'organizzazione.\"}]",
        )

        # organizzato_da_esterno is considered empty block
        data.update(
            {
                "organizzato_da_esterno": {
                    "blocks": {
                        "b8850749-4d5f-4b5f-b842-c050bcf7fd6f": {"@type": "slate"}
                    },
                    "blocks_layout": {
                        "items": ["b8850749-4d5f-4b5f-b842-c050bcf7fd6f"]
                    },
                },
                "organizzato_da_interno": [],
            }
        )

        resp = self.api_session.post(self.portal_url, json=data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json()["message"],
            "[{'field': 'organizzato_da_esterno', 'message': \"Devi compilare almeno uno dei due campi per l'organizzazione.\"}, {'field': 'organizzato_da_interno', 'message': \"Devi compilare almeno uno dei due campi per l'organizzazione.\"}]",
        )

        # now compile only organizzato_da_interno
        data["organizzato_da_interno"] = [{"@id": "/pdc"}]
        resp = self.api_session.post(self.portal_url, json=data)
        self.assertEqual(resp.status_code, 201)

        # and compile only organizzato_da_esterno
        data["organizzato_da_interno"] = []
        data["organizzato_da_esterno"] = {
            "blocks": {
                "b8850749-4d5f-4b5f-b842-c050bcf7fd6f": {
                    "@type": "slate",
                    "text": "xxx",
                }
            },
        }
        resp = self.api_session.post(self.portal_url, json=data)
        self.assertEqual(resp.status_code, 201)

    def test_raise_bad_request_if_missing_a_chi_si_rivolge_fields(self):

        pdc = api.content.create(
            type="PuntoDiContatto", title="pdc", container=self.portal
        )
        commit()
        data = {
            "come_accedere": {"blocks": {}},
            "orari_apertura": {"blocks": {}},
            "description": "asdasd",
            "punti_di_contatto": [{"@id": "/pdc"}],
            "title": "titolo",
            "@type": "Struttura",
        }
        resp = self.api_session.post(self.portal_url, json=data)

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json()["message"],
            "[{'field': 'a_chi_si_rivolge', 'message': 'Devi compilare almeno uno dei due campi di \"A chi si rivolge\".'}, {'field': 'a_chi_si_rivolge_tassonomia', 'message': 'Devi compilare almeno uno dei due campi di \"A chi si rivolge\".'}]",
        )

        # a_chi_si_rivolge is considered empty block
        data.update(
            {
                "a_chi_si_rivolge": {
                    "blocks": {
                        "b8850749-4d5f-4b5f-b842-c050bcf7fd6f": {"@type": "slate"}
                    },
                    "blocks_layout": {
                        "items": ["b8850749-4d5f-4b5f-b842-c050bcf7fd6f"]
                    },
                },
                "a_chi_si_rivolge_tassonomia": [],
            }
        )

        resp = self.api_session.post(self.portal_url, json=data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json()["message"],
            "[{'field': 'a_chi_si_rivolge', 'message': 'Devi compilare almeno uno dei due campi di \"A chi si rivolge\".'}, {'field': 'a_chi_si_rivolge_tassonomia', 'message': 'Devi compilare almeno uno dei due campi di \"A chi si rivolge\".'}]",
        )

        # now compile only a_chi_si_rivolge_tassonomia
        data["a_chi_si_rivolge_tassonomia"] = ["anziani"]
        resp = self.api_session.post(self.portal_url, json=data)
        self.assertEqual(resp.status_code, 201)

        # and compile only a_chi_si_rivolge
        data["a_chi_si_rivolge_tassonomia"] = []
        data["a_chi_si_rivolge"] = {
            "blocks": {
                "b8850749-4d5f-4b5f-b842-c050bcf7fd6f": {
                    "@type": "slate",
                    "text": "xxx",
                }
            },
        }
        resp = self.api_session.post(self.portal_url, json=data)
        self.assertEqual(resp.status_code, 201)
