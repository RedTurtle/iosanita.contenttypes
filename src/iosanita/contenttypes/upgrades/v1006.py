# -*- coding: utf-8 -*-

from . import logger
from plone.app.upgrade.utils import installOrReinstallProduct
from plone import api


def upgrade(setup_tool=None):
    """ """
    logger.info("Install blocksfield")
    installOrReinstallProduct(api.portal.get(), "collective.volto.blocksfield")
