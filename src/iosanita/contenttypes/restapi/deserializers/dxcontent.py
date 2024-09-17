from iosanita.contenttypes.interfaces import IIosanitaContenttypesLayer
from iosanita.contenttypes.interfaces import IoSanitaMigrationMarker
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi import _
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.dxcontent import DeserializeFromJson as BaseDeserializer
from plone.restapi.interfaces import IDeserializeFromJson
from zExceptions import BadRequest
from zope.component import adapter
from zope.interface import implementer

import json


@implementer(IDeserializeFromJson)
@adapter(IDexterityContent, IIosanitaContenttypesLayer)
class DeserializeFromJson(BaseDeserializer):
    def __call__(
        self, validate_all=False, data=None, create=False, mask_validation_errors=True
    ):
        if data is None:
            data = json_body(self.request)
        # iosanità validations
        self.validate_data_iosanita(data=data, create=create)

        return super().__call__(
            validate_all=validate_all,
            data=data,
            create=create,
            mask_validation_errors=mask_validation_errors,
        )

    def validate_data_iosanita(self, data, create):
        if IoSanitaMigrationMarker.providedBy(self.request):
            return
        if create:
            portal_type = data.get("@type", "")
        else:
            portal_type = self.context.portal_type

        self.validate_a_chi_si_rivolge(
            portal_type=portal_type, data=data, create=create
        )

        if portal_type == "Event":
            self.validate_event(data=data, create=create)

    def validate_a_chi_si_rivolge(self, portal_type, data, create):
        portal_types = api.portal.get_tool(name="portal_types")
        behaviors = portal_types[portal_type].behaviors

        has_behaviors = False
        for bhv in [
            "iosanita.contenttypes.behavior.a_chi_si_rivolge",
            "collective.taxonomy.generated.a_chi_si_rivolge_tassonomia",
        ]:
            if bhv in behaviors:
                has_behaviors = True
        if not has_behaviors:
            # skip check
            return

        a_chi_si_rivolge = data.get("a_chi_si_rivolge", {})
        a_chi_si_rivolge_tassonomia = data.get("a_chi_si_rivolge_tassonomia", [])

        if not create:
            if not a_chi_si_rivolge:
                a_chi_si_rivolge = getattr(self.context, "a_chi_si_rivolge", {})
            if not a_chi_si_rivolge_tassonomia:
                a_chi_si_rivolge_tassonomia = getattr(
                    self.context, "a_chi_si_rivolge_tassonomia", []
                )
        if self.is_empty_blocks(a_chi_si_rivolge) and not a_chi_si_rivolge_tassonomia:
            msg = api.portal.translate(
                _(
                    "a_chi_si_rivolge_validation_error",
                    default='Devi compilare almeno uno dei due campi del tab "A chi si rivolge".',
                )
            )
            # temporaneamente commentato perché Volto non lo gestisce bene
            # raise BadRequest(
            # json.dumps(
            #     [
            #         {"field": "a_chi_si_rivolge", "message": msg},
            #         {"field": "a_chi_si_rivolge_tassonomia", "message": msg},
            #     ]
            # )
            # )
            raise BadRequest(json.dumps({"error": {"message": msg}}))

    def validate_event(self, data, create):
        # validate organizzato da
        if not create:
            if (
                "organizzato_da_esterno" not in data
                and "organizzato_da_interno" not in data  # noqa
            ):
                return

            if (
                "webinar" not in data
                and "struttura_correlata" not in data  # noqa
                and "geolocation" not in data  # noqa
            ):
                return

        organizzato_da_esterno = data.get("organizzato_da_esterno", {})
        organizzato_da_interno = data.get("organizzato_da_interno", [])

        if self.is_empty_blocks(organizzato_da_esterno) and not organizzato_da_interno:
            msg = api.portal.translate(
                _(
                    "organizzato_validation_error",
                    default='Devi compilare almeno uno dei due campi per "Organizzato da" nel tab "Contatti".',
                )
            )
            # temporaneamente commentato perché Volto non lo gestisce bene
            # raise BadRequest(
            #     [
            #         {"field": "organizzato_da_esterno", "message": msg},
            #         {"field": "organizzato_da_interno", "message": msg},
            #     ]
            # )
            raise BadRequest(json.dumps({"error": {"message": msg}}))

        # validate dove
        has_webinar = not self.is_empty_blocks(data.get("webinar", {}))
        has_struttura_correlata = data.get("struttura_correlata", [])
        has_location_infos = self.has_location_infos(data)
        if not has_webinar and not has_struttura_correlata and not has_location_infos:
            msg = api.portal.translate(
                _(
                    "dove_event_validation_error",
                    default='Devi compilare almeno uno tra i campi "Webinar", "Struttura di riferimento" o "Geolocation" del tab "Dove".',
                )
            )
            raise BadRequest(json.dumps({"error": {"message": msg}}))

    def has_location_infos(self, data):
        has_data = True
        for fieldname in ["geolocation"]:
            value = data.get(fieldname, None)
            if not value or value in [{"latitude": 0, "longitude": 0}]:
                has_data = False
        return has_data

    def is_empty_blocks(self, blocks_field):
        blocks = blocks_field.get("blocks", {})
        if not blocks:
            return True
        blocks_data = list(blocks.values())
        for block in blocks_data:
            if block.get("plaintext", ""):
                # there is some text
                return False
        return True
