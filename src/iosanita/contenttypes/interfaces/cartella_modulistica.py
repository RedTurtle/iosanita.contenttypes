# -*- coding: utf-8 -*-
from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces import IIosanitaContenttypes
from plone.supermodel import model
from zope import schema


class ICartellaModulistica(model.Schema, IIosanitaContenttypes):
    """Cartella Modulistica"""

    anteprima_file = schema.Bool(
        title=_("anteprima_file_title", default="Mostra i PDF in anteprima"),
        description=_(
            "anteprima_file_description",
            default="Permette di aprire l'anteprima di tutti i PDF di questa cartella"
            " in una tab separata, altrimenti i PDF vengono scaricati",
        ),
        required=False,
        default=False,
    )
