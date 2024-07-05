# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from collective.taxonomy.interfaces import ITaxonomy
from zope.component import getUtilitiesFor
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "iosanita.contenttypes:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["iosanita.contenttypes.upgrades"]


def post_install(context):
    """Post install script"""

    # Do something at the end of the installation of this package.


def post_install_taxonomy(context):
    import pdb

    pdb.set_trace()
    context.runImportStepFromProfile(
        "profile-iosanita.contenttypes:default", "typeinfo", True
    )
    # C'è una versione di collective.taxonomies in cui quel campo non viene
    # settato correttamente.
    for utility_name, utility in list(getUtilitiesFor(ITaxonomy)):
        utility.updateBehavior(**{"field_prefix": ""})


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
