# -*- coding: utf-8 -*-
from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces import IIosanitaContenttypes
from plone.supermodel import model
from zope import schema


class IModulo(model.Schema, IIosanitaContenttypes):
    """Modulo"""
