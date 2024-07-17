from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from zope.configuration import xmlconfig

import plone.restapi
import collective.venue
import collective.volto.blocksfield
import collective.volto.cookieconsent
import collective.z3cform.datagridfield
import kitconcept.seo
import plone.app.caching
import plone.formwidget.geolocation
import iosanita.contenttypes
from redturtle.volto.testing import RedturtleVoltoLayer


class TestLayer(RedturtleVoltoLayer):

    def setUpZope(self, app, configurationContext):
        super().setUpZope(app, configurationContext)
        self.loadZCML(package=iosanita.contenttypes, context=configurationContext)
        self.loadZCML(package=collective.taxonomy)
        self.loadZCML(package=collective.venue)
        self.loadZCML(package=collective.volto.blocksfield)
        self.loadZCML(package=collective.z3cform.datagridfield)
        self.loadZCML(package=kitconcept.seo)
        self.loadZCML(package=plone.formwidget.geolocation)
        xmlconfig.file(
            "configure.zcml",
            iosanita.contenttypes,
            context=configurationContext,
        )

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)
        applyProfile(portal, "iosanita.contenttypes:default")


FIXTURE = TestLayer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="IoSanitaContenttypesLayer:IntegrationTesting",
)


FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name="IoSanitaContenttypesLayer:FunctionalTesting",
)

RESTAPI_TESTING = FunctionalTesting(
    bases=(FIXTURE, WSGI_SERVER_FIXTURE),
    name="IoSanitaContenttypesLayer:RestAPITesting",
)
