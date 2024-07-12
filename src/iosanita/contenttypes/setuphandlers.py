# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from collective.taxonomy.interfaces import ITaxonomy
from zope.component import getUtilitiesFor
from zope.interface import implementer
from plone import api

import logging

logger = logging.getLogger(__name__)
DEFAULT_PROFILE = "profile-iosanita.contenttypes:default"


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


class colors(object):
    GREEN = "\033[92m"
    ENDC = "\033[0m"
    RED = "\033[91m"
    DARKCYAN = "\033[36m"
    YELLOW = "\033[93m"


def update_profile(context, profile, run_dependencies=True):
    context.runImportStepFromProfile(DEFAULT_PROFILE, profile, run_dependencies)


def update_types(context):
    update_profile(context, "typeinfo")


def update_registry(context):
    update_profile(context, "plone.app.registry", run_dependencies=False)


def update_catalog(context):
    update_profile(context, "catalog")


def post_install(context):
    """Post install script"""

    context.runImportStepFromProfile(
        "iosanita.contenttypes:taxonomy", "collective.taxonomy"
    )

    # for utility_name, utility in list(getUtilitiesFor(ITaxonomy)):
    #     utility.updateBehavior(**{"field_prefix": ""})
    #     logger.info(
    #         f"{colors.DARKCYAN} Change taxonomy prefix for {utility_name} {colors.ENDC}"  # noqa
    #     )

    # logger.info(
    #     f"{colors.DARKCYAN} iosanita.contentypes taxonomies imported {colors.ENDC}"  # noqa
    # )
    # update_types(context)
    # update_registry(context)
    # update_catalog(context)

    # Do something at the end of the installation of this package.


def post_install_taxonomy(context):

    try:
        for index in [
            "tipologia_notizia",
            "tipologia_target",
            "tipologia_argomento",
            "tipologia_evento",
            "tipologia_punti_di_contatto",
        ]:
            api.portal.get_tool("portal_catalog").delIndex(index)
    # NOTE: non va bene, cosa è che si rompe
    except:  # noqa
        pass

    for utility_name, utility in list(getUtilitiesFor(ITaxonomy)):
        utility.updateBehavior(**{"field_prefix": ""})
        logger.info(
            f"{colors.DARKCYAN} Change taxonomy prefix for {utility_name} {colors.ENDC}"  # noqa
        )

    logger.info(
        f"{colors.DARKCYAN} iosanita.contentypes taxonomies imported {colors.ENDC}"  # noqa
    )
    update_types(context)
    update_registry(context)
    update_catalog(context)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
