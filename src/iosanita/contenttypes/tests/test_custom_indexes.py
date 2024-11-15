# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from iosanita.contenttypes.testing import INTEGRATION_TESTING
from plone import api
from plone.app.dexterity.behaviors.metadata import IDublinCore
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.event import notify
from zope.lifecycleevent import Attributes
from zope.lifecycleevent import ObjectModifiedEvent
from plone.indexer.interfaces import IIndexableObject
from zope.component import queryMultiAdapter
from plone.formwidget.geolocation.geolocation import Geolocation
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.event import notify
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent

import unittest


class TestCustomIndexes(unittest.TestCase):
    """"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.catalog = api.portal.get_tool(name="portal_catalog")
        self.intids = getUtility(IIntIds)

    def test_parent_metadata_has_parent_data(self):
        parent = api.content.create(
            container=self.portal,
            type="Document",
            title="Parent",
        )

        child = api.content.create(
            container=parent,
            type="Document",
            title="Child",
        )

        brain = api.content.find(UID=child.UID())[0]

        self.assertEqual(
            sorted(["title", "UID", "@id", "@type"]), sorted(list(brain.parent.keys()))
        )
        self.assertEqual(brain.parent["title"], "Parent")
        self.assertEqual(brain.parent["UID"], parent.UID())

    def test_when_parent_changes_children_will_be_updated(self):
        parent = api.content.create(
            container=self.portal,
            type="Document",
            title="Parent",
        )

        child = api.content.create(
            container=parent,
            type="Document",
            title="Child",
        )

        brain = api.content.find(UID=child.UID())[0]
        self.assertEqual(brain.parent["title"], "Parent")

        # update title
        parent.title = "New Parent Title"
        descriptions = [Attributes(IDublinCore, *["IDublinCore.title"])]
        notify(ObjectModifiedEvent(parent, *descriptions))

        brain = api.content.find(UID=child.UID())[0]
        self.assertEqual(brain.parent["title"], "New Parent Title")

    def test_has_geolocation_false_if_geolocation_is_not_set(self):
        item = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Struttura",
        )
        adapter = queryMultiAdapter((item, self.catalog), IIndexableObject)
        self.assertFalse(adapter.has_geolocation)

    def test_has_geolocation_false_if_geolocation_is_set_as_0(self):
        item = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Struttura",
        )
        adapter = queryMultiAdapter((item, self.catalog), IIndexableObject)
        self.assertFalse(adapter.has_geolocation)

        item.geolocation = Geolocation(latitude=0, longitude=0)

        item.reindexObject()

        adapter = queryMultiAdapter((item, self.catalog), IIndexableObject)
        self.assertFalse(adapter.has_geolocation)

    def test_has_geolocation_true_if_geolocation_is_set(self):
        item = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Struttura",
        )
        adapter = queryMultiAdapter((item, self.catalog), IIndexableObject)
        self.assertFalse(adapter.has_geolocation)

        item.geolocation = Geolocation(latitude=10, longitude=10)

        item.reindexObject()

        self.assertTrue(adapter.has_geolocation)

    def test_has_geolocation_for_persona_false_if_has_no_dove_fields_compiled(
        self,
    ):
        item = api.content.create(
            container=self.portal,
            type="Persona",
            title="Persona",
        )
        adapter = queryMultiAdapter((item, self.catalog), IIndexableObject)
        self.assertFalse(adapter.has_geolocation)

    def test_has_geolocation_for_persona_false_if_geolocation_is_set_as_0(self):
        item = api.content.create(
            container=self.portal,
            type="Persona",
            title="Persona",
        )
        adapter = queryMultiAdapter((item, self.catalog), IIndexableObject)
        self.assertFalse(adapter.has_geolocation)

        item.geolocation = Geolocation(latitude=0, longitude=0)

        item.reindexObject()

        adapter = queryMultiAdapter((item, self.catalog), IIndexableObject)
        self.assertFalse(adapter.has_geolocation)

    def test_has_geolocation_for_persona_true_if_geolocation_is_set(self):
        item = api.content.create(
            container=self.portal,
            type="Persona",
            title="Persona",
        )
        adapter = queryMultiAdapter((item, self.catalog), IIndexableObject)
        self.assertFalse(adapter.has_geolocation)

        item.geolocation = Geolocation(latitude=10, longitude=10)

        item.reindexObject()

        adapter = queryMultiAdapter((item, self.catalog), IIndexableObject)
        self.assertTrue(adapter.has_geolocation)

    def test_has_geolocation_for_persona_true_if_struttura_in_cui_opera_is_set(self):
        struttura = api.content.create(
            container=self.portal, type="Struttura", title="Struttura"
        )
        item = api.content.create(
            container=self.portal,
            type="Persona",
            title="Persona",
        )
        adapter = queryMultiAdapter((item, self.catalog), IIndexableObject)
        self.assertFalse(adapter.has_geolocation)

        item.struttura_in_cui_opera = [RelationValue(self.intids.getId(struttura))]

        notify(ObjectModifiedEvent(item))
        item.reindexObject()

        adapter = queryMultiAdapter((item, self.catalog), IIndexableObject)
        self.assertTrue(adapter.has_geolocation)

    def test_has_geolocation_for_persona_true_if_struttura_ricevimento_is_set(self):
        struttura = api.content.create(
            container=self.portal, type="Struttura", title="Struttura"
        )
        item = api.content.create(
            container=self.portal,
            type="Persona",
            title="Persona",
        )
        adapter = queryMultiAdapter((item, self.catalog), IIndexableObject)
        self.assertFalse(adapter.has_geolocation)

        item.struttura_ricevimento = [RelationValue(self.intids.getId(struttura))]

        notify(ObjectModifiedEvent(item))
        item.reindexObject()

        adapter = queryMultiAdapter((item, self.catalog), IIndexableObject)
        self.assertTrue(adapter.has_geolocation)

    def test_geolocation_metadata_is_empty_if_no_geolocation_set(self):
        struttura = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Struttura",
        )

        brain = api.content.find(UID=struttura.UID())[0]
        self.assertEqual(brain.geolocation, [])

    def test_geolocation_metadata_has_geolocation_data(self):
        struttura = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Struttura",
            geolocation=Geolocation(latitude=10, longitude=20),
        )

        brain = api.content.find(UID=struttura.UID())[0]
        self.assertEqual(len(brain.geolocation), 1)
        self.assertEqual(
            brain.geolocation[0]["latitude"], struttura.geolocation.latitude
        )
        self.assertEqual(
            brain.geolocation[0]["longitude"], struttura.geolocation.longitude
        )

    def test_geolocation_metadata_has_content_address_with_street_city_provincia(self):
        struttura = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Struttura",
            street="Elm Street, 4",
            city="Springwood",
            provincia="FE",
            geolocation=Geolocation(latitude=10, longitude=20),
        )

        brain = api.content.find(UID=struttura.UID())[0]
        self.assertEqual(len(brain.geolocation), 1)
        self.assertEqual(
            brain.geolocation[0]["address"], "Elm Street, 4 Springwood (FE)"
        )

    def test_geolocation_metadata_has_content_nome_sede_or_title(self):
        struttura = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Struttura",
            geolocation=Geolocation(latitude=10, longitude=20),
        )

        brain = api.content.find(UID=struttura.UID())[0]
        self.assertEqual(len(brain.geolocation), 1)
        self.assertEqual(brain.geolocation[0]["title"], struttura.title)

        struttura.nome_sede = "Nightmare, inc."
        struttura.reindexObject()

        brain = api.content.find(UID=struttura.UID())[0]
        self.assertEqual(brain.geolocation[0]["title"], struttura.nome_sede)

    def test_geolocation_metadata_for_persona_has_a_list_of_values_if_set(self):
        struttura1 = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Struttura",
            geolocation=Geolocation(latitude=11, longitude=11),
        )
        struttura2 = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Struttura",
            geolocation=Geolocation(latitude=22, longitude=22),
        )
        struttura3 = api.content.create(
            container=self.portal,
            type="Struttura",
            title="Struttura",
            geolocation=Geolocation(latitude=33, longitude=33),
        )

        persona = api.content.create(
            container=self.portal,
            type="Persona",
            title="persona",
            geolocation=Geolocation(latitude=99, longitude=99),
            struttura_ricevimento=[
                RelationValue(self.intids.getId(struttura1)),
                RelationValue(self.intids.getId(struttura2)),
            ],
            struttura_in_cui_opera=[RelationValue(self.intids.getId(struttura3))],
        )

        brain = api.content.find(UID=persona.UID())[0]

        geolocations = brain.geolocation
        self.assertEqual(len(geolocations), 4)
        self.assertEqual(geolocations[0]["latitude"], persona.geolocation.latitude)
        self.assertEqual(geolocations[0]["longitude"], persona.geolocation.longitude)
        self.assertEqual(geolocations[1]["latitude"], struttura3.geolocation.latitude)
        self.assertEqual(geolocations[1]["longitude"], struttura3.geolocation.longitude)
        self.assertEqual(geolocations[2]["latitude"], struttura1.geolocation.latitude)
        self.assertEqual(geolocations[2]["longitude"], struttura1.geolocation.longitude)
        self.assertEqual(geolocations[3]["latitude"], struttura2.geolocation.latitude)
        self.assertEqual(geolocations[3]["longitude"], struttura2.geolocation.longitude)
