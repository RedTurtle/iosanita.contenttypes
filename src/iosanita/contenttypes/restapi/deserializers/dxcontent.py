from plone.restapi.deserializer.dxcontent import DeserializeFromJson as BaseDeserializer
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi import _
from plone.restapi.interfaces import IDeserializeFromJson
from zope.component import adapter
from zope.interface import implementer
from iosanita.contenttypes.interfaces import IIosanitaContenttypesLayer
from zExceptions import BadRequest
from plone.restapi.deserializer import json_body
from plone import api


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
        # if errors:
        #     if mask_validation_errors:
        #         # Drop Python specific error classes in order to be able to better handle
        #         # errors on front-end
        #         for error in errors:
        #             error["error"] = "ValidationError"
        #     for error in errors:
        #         error["message"] = translate(error["message"], context=self.request)
        #     raise BadRequest(errors)

        return super().__call__(
            validate_all=validate_all,
            data=data,
            create=create,
            mask_validation_errors=mask_validation_errors,
        )

    def validate_data_iosanita(self, data, create):

        if not create:
            portal_type = self.context.portal_type
        else:
            portal_type = data.get("@type", "")

        self.validate_a_chi_si_rivolge(data=data, create=create)

        if portal_type == "Event":
            self.validate_event(data=data, create=create)

    def validate_a_chi_si_rivolge(self, data, create):
        if not create:
            if (
                "a_chi_si_rivolge" not in data
                and "a_chi_si_rivolge_tassonomia" not in data
            ):
                return
        a_chi_si_rivolge = data.get("a_chi_si_rivolge", {})
        a_chi_si_rivolge_tassonomia = data.get("a_chi_si_rivolge_tassonomia", [])

        if self.is_empty_blocks(a_chi_si_rivolge) and not a_chi_si_rivolge_tassonomia:
            msg = api.portal.translate(
                _(
                    "a_chi_si_rivolge_validation_error",
                    default='Devi compilare almeno uno dei due campi di "A chi si rivolge".',
                )
            )
            raise BadRequest(
                [
                    {"field": "a_chi_si_rivolge", "message": msg},
                    {"field": "a_chi_si_rivolge_tassonomia", "message": msg},
                ]
            )

    def validate_event(self, data, create):
        # validate organizzato da
        if not create:
            if (
                "organizzato_da_esterno" not in data
                and "organizzato_da_interno" not in data
            ):
                return

        organizzato_da_esterno = data.get("organizzato_da_esterno", {})
        organizzato_da_interno = data.get("organizzato_da_interno", [])

        if self.is_empty_blocks(organizzato_da_esterno) and not organizzato_da_interno:
            msg = api.portal.translate(
                _(
                    "organizzato_validation_error",
                    default="Devi compilare almeno uno dei due campi per l'organizzazione.",
                )
            )
            raise BadRequest(
                [
                    {"field": "organizzato_da_esterno", "message": msg},
                    {"field": "organizzato_da_interno", "message": msg},
                ]
            )

    def is_empty_blocks(self, blocks_field):
        blocks = blocks_field.get("blocks", {})
        if not blocks:
            return True
        blocks_data = list(blocks.values())
        if len(blocks_data) == 1:
            if blocks_data[0] == {"@type": "slate"}:
                return True
        return False
