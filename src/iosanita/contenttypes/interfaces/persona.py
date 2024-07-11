# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from iosanita.contenttypes import _
from iosanita.contenttypes.interfaces import IIosanitaContenttypes
from plone.app.dexterity import textindexer
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.namedfile import field
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema


# TODO: migration script for these commented fields towards PDC
# telefono
# fax
# email
# TODO: migration script for these commented fields towards Incarico
# atto_nomina
# data_conclusione_incarico
# data_insediamento


class IPersona(model.Schema, IIosanitaContenttypes):
    """Marker interface for contenttype Persona"""

    sottotitolo = schema.TextLine(
        title=_("sottotitolo_label", default="Sottotitolo"),
        description=_(
            "sottotitolo_help",
            default="Indica un eventuale sottotitolo/titolo alternativo.",
        ),
        required=True,
    )

    foto_persona = field.NamedBlobImage(
        title=_("foto_persona_label", default="Foto della persona"),
        required=False,
        description=_(
            "foto_persona_help",
            default="Foto da mostrare della persona. "
            "La dimensione suggerita è 100x180px.",
        ),
    )

    incarichi = BlocksField(
        title=_("incarichi_label", default="Incarichi"),
        description=_(
            "incarichi_help",
            default="Indicazione degli incarichi della persona all'interno dell'ASL.",
        ),
        required=False,
    )

    orari_di_ricevimento = BlocksField(
        title=_("orari_di_ricevimento_label", default="Orari di ricevimento"),
        description=_(
            "orari_di_ricevimento_help",
            default="Orari durante i quali è possibile incontrare la persona descritta, se effettua ricevimento.",
        ),
        required=False,
    )

    biografia = BlocksField(
        title=_("biografia_label", default="Biografia"),
        description=_(
            "biografia_help",
            default="Solo per persona politica: testo descrittivo che riporta"
            " la biografia della persona.",
        ),
        required=False,
    )

    # Questo campo per direttive e richieste viene nascosto nella form
    # Lo si tiene perche si vuole evitare di perder dati tra le migrazioni
    # e magari non poter piu' usare la feature collegata, ossia
    # la check persone, in quanto relazioni potrebbero rompersi o perdersi
    organizzazione_riferimento = RelationList(
        title=_(
            "organizzazione_riferimento_label",
            default="Unità organizzativa di appartenenza",
        ),
        description=_(
            "organizzazione_riferimento_help",
            default="Seleziona una lista di organizzazioni a cui la persona"
            " appartiene.",
        ),
        value_type=RelationChoice(
            title=_("Organizzazione di riferimento"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        default=[],
        required=False,
    )

    competenze = BlocksField(
        title=_("competenze_label", default="Competenze"),
        description=_(
            "competenze_help",
            default="Descrizione del ruolo e dei compiti della persona.",
        ),
        required=False,
    )

    biografia = BlocksField(
        title=_("biografia_label", default="Biografia"),
        description=_(
            "biografia_help",
            default="Solo per persona politica: testo descrittivo che riporta"
            " la biografia della persona.",
        ),
        required=False,
    )

    curriculum_vitae = field.NamedBlobFile(
        title=_("curriculum_vitae_label", default="Curriculum vitae"),
        required=False,
        description=_(
            "curriculum_vitae_help",
            default="Allega un file contenente il curriculum vitae della persona. "
            "Se ha più file da allegare, utilizza questo campo per quello principale "
            'e gli altri mettili dentro alla cartella "Curriculum vitae" che troverai dentro alla Persona.',  # noqa
        ),
    )

    # custom widgets
    form.widget(
        "organizzazione_riferimento",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    # custom fieldsets
    model.fieldset(
        "ruolo",
        label=_("ruolo_label", default="Ruolo"),
        fields=[
            "organizzazione_riferimento",
            "competenze",
            "biografia",
        ],
    )
    model.fieldset(
        "documenti",
        label=_("documenti_label", default="Documenti"),
        fields=["curriculum_vitae"],
    )

    # SearchableText fields
    textindexer.searchable("competenze")
    # TODO: migration script for these commented fields towards PDC
    # textindexer.searchable("telefono")
    # textindexer.searchable("fax")
    # textindexer.searchable("email")
