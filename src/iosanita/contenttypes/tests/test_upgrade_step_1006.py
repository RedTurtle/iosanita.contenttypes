# -*- coding: utf-8 -*-
# from iosanita.contenttypes.testing import IOSANITA_CONTENTTYPES_FUNCTIONAL_TESTING
from iosanita.contenttypes.testing import IOSANITA_CONTENTTYPES_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class UpgradeStepIntegrationTest(unittest.TestCase):
    layer = IOSANITA_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_upgrade_step(self):
        # dummy, add tests here
        self.assertTrue(True)


# class UpgradeStepFunctionalTest(unittest.TestCase):
#
#     layer = IOSANITA_CONTENTTYPES_FUNCTIONAL_TESTING
#
#     def setUp(self):
#         self.portal = self.layer['portal']
#         setRoles(self.portal, TEST_USER_ID, ['Manager'])
