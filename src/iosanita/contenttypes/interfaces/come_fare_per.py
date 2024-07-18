# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces import IIosanitaContenttypes
from plone.supermodel import model
from plone.autoform import directives as form


class IComeFarePer(model.Schema, IIosanitaContenttypes):
    """Marker interface for content type"""

    panoramica = BlocksField(
        title=_("panoramica_label", default="Panoramica"),
        description=_(
            "panoramica_help",
            default="Descrizione più estesa della procedura di cui viene descritto il processo di usufruizione.",
        ),
        required=True,
    )

    form.order_after(panoramica="sottotitolo")
