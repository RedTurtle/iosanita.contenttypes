# -*- coding: utf-8 -*-

from . import logger
from iosanita.contenttypes.events.common import SUBFOLDERS_MAPPING
from plone import api


def upgrade(setup_tool=None):
    """ """
    logger.info("Running upgrade (Python): Exclude auto-created subfolders from search")

    fixed = 0
    for parent_type, mapping in SUBFOLDERS_MAPPING.items():
        subfolders = {x["id"]: x.get("type", "Document") for x in mapping["content"]}
        for brain in api.content.find(portal_type=parent_type):
            parent = brain.getObject()
            for child_id, child_type in subfolders.items():
                child = parent.get(child_id, None)
                if child is None or child.portal_type != child_type:
                    continue
                if _exclude_from_search(child):
                    fixed += 1

    # "Bando Folder Deepening" can be created also manually.
    for brain in api.content.find(portal_type="Bando Folder Deepening"):
        if _exclude_from_search(brain.getObject()):
            fixed += 1

    logger.info(f"Done: {fixed} subfolders excluded from search")


def _exclude_from_search(item):
    if getattr(item.aq_base, "exclude_from_search", False):
        return False
    item.exclude_from_search = True
    item.reindexObject(idxs=["exclude_from_search"])
    return True
