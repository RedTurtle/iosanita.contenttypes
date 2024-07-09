# -*- coding: utf-8 -*-
from collective.geolocationbehavior.geolocation import IGeolocatable
from iosanita.contenttypes import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IGeolocatableEvent(IGeolocatable):
    model.fieldset(
        "luogo",
        label=_("luogo_label", default="Luogo"),
        fields=["geolocation"],
    )


@implementer(IGeolocatableEvent)
@adapter(IDexterityContent)
class GeolocatableEvent(object):
    """ """

    def __init__(self, context):
        self.context = context


@provider(IFormFieldProvider)
class IGeolocatablePersona(IGeolocatable):
    model.fieldset(
        "dove",
        label=_("dove_label", default="Dove"),
        fields=["geolocation"],
    )

@implementer(IGeolocatablePersona)
@adapter(IDexterityContent)
class GeolocatablePersona(object):
    """ """

    def __init__(self, context):
        self.context = context