# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import iosanita.contenttypes


class IosanitaContenttypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=iosanita.contenttypes)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "iosanita.contenttypes:default")


IOSANITA_CONTENTTYPES_FIXTURE = IosanitaContenttypesLayer()


IOSANITA_CONTENTTYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IOSANITA_CONTENTTYPES_FIXTURE,),
    name="IosanitaContenttypesLayer:IntegrationTesting",
)


IOSANITA_CONTENTTYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IOSANITA_CONTENTTYPES_FIXTURE,),
    name="IosanitaContenttypesLayer:FunctionalTesting",
)


IOSANITA_CONTENTTYPES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        IOSANITA_CONTENTTYPES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="IosanitaContenttypesLayer:AcceptanceTesting",
)
