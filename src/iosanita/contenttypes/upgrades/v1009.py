# -*- coding: utf-8 -*-

from . import logger
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile


def upgrade(setup_tool=None):
    """ """
    logger.info("Running upgrade: Add distretto and city catalog indexes")
    loadMigrationProfile(api.portal.get(), "iosanita.contenttypes.upgrades:1009")

    brains = api.content.find(
        object_provides="iosanita.contenttypes.behaviors.dove.IDove"
    )
    i = 0
    tot = len(brains)
    logger.info(f"Reindexing distretto and city on {tot} objects")
    for brain in brains:
        i += 1
        if i % 100 == 0:
            logger.info(f"Progress: {i}/{tot}")
        obj = brain.getObject()
        obj.reindexObject(idxs=["distretto", "city"])
    logger.info("Done reindexing distretto and city")
