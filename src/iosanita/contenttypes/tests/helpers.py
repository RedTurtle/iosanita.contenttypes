# -*- coding: utf-8 -*-
from importlib.metadata import version as pkg_version
from packaging.version import Version

# True when volto.preview_image behavior defines its own "preview_image"
# fieldset (plone.volto >= 5.1.0), so preview fields are no longer in default.
HAS_VOLTO_PREVIEW_FIELDSET = Version(pkg_version("plone.volto")) >= Version("5.1.0")
