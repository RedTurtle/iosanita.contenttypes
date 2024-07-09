# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
# from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

from redturtle.volto.testing import RedturtleVoltoLayer
from redturtle.volto.testing import RedturtleVoltoRestApiLayer
from zope.configuration import xmlconfig

import collective.address
import collective.taxonomy

# import collective.folderishtypes
import collective.venue
import collective.volto.blocksfield
import collective.volto.cookieconsent
import collective.volto.enhancedlinks
import collective.z3cform.datagridfield
import kitconcept.seo
import plone.app.caching
import plone.formwidget.geolocation
# import redturtle.volto

import iosanita.contenttypes


class IosanitaContenttypesLayer(RedturtleVoltoLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        super().setUpZope(app, configurationContext)
        self.loadZCML(package=collective.venue)
        self.loadZCML(package=collective.volto.blocksfield)
        self.loadZCML(package=collective.volto.enhancedlinks)
        self.loadZCML(package=iosanita.contenttypes, context=configurationContext)
        self.loadZCML(package=plone.formwidget.geolocation)
        # self.loadZCML(name="overrides.zcml", package=iosanita.contenttypes)
        xmlconfig.file(
            "configure.zcml",
            iosanita.contenttypes,
            context=configurationContext,
        )
        self.loadZCML(package=kitconcept.seo)
        self.loadZCML(package=collective.taxonomy)
        self.loadZCML(package=collective.z3cform.datagridfield)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)
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


class IoSanitaContenttypesRestApiLayer(RedturtleVoltoRestApiLayer):
    def setUpZope(self, app, configurationContext):
        super().setUpZope(app, configurationContext)
        self.loadZCML(package=collective.venue)
        self.loadZCML(package=collective.volto.blocksfield)
        self.loadZCML(package=collective.volto.enhancedlinks)
        self.loadZCML(package=iosanita.contenttypes, context=configurationContext)
        self.loadZCML(package=plone.formwidget.geolocation)
        self.loadZCML(package=collective.taxonomy)
        self.loadZCML(package=collective.z3cform.datagridfield)
        xmlconfig.file(
            "configure.zcml",
            iosanita.contenttypes,
            context=configurationContext,
        )
        self.loadZCML(package=kitconcept.seo)

        # self.loadZCML(name="overrides.zcml", package=iosanita.contenttypes)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)
        applyProfile(portal, "iosanita.contenttypes:default")


IOSANITA_CONTENTTYPES_API_FIXTURE = IoSanitaContenttypesRestApiLayer()
IOSANITA_CONTENTTYPES_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IOSANITA_CONTENTTYPES_API_FIXTURE,),
    name="DesignPloneContenttypesRestApiLayer:Integration",
)

IOSANITA_CONTENTTYPES_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IOSANITA_CONTENTTYPES_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="DesignPloneContenttypesRestApiLayer:Functional",
)
