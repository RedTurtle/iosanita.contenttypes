# -*- coding: utf-8 -*-
from iosanita.contenttypes import _
from plone.restapi.services.types.get import TypesGet as BaseGet
from zope.i18n import translate
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


class FieldsetsMismatchError(Exception):
    """Exception thrown when we try to reorder fieldsets, but the order list is
    different from the fieldsets returned from Plone
    """


FIELDSETS_ORDER = {
    "ComeFarePer": [
        "default",
        "utenti",
        "ulteriori_informazioni",
        "categorization",
        "dates",
        "settings",
        "ownership",
    ],
    "Event": [
        "default",
        "cose",
        "partecipanti",
        "dove",
        "costi",
        "contatti",
        "ulteriori_informazioni",
        "contenuti_collegati",
        "categorization",
        "dates",
        "settings",
        "ownership",
    ],
    "Struttura": [
        "default",
        "cosa_e",
        "a_chi_si_rivolge",
        "dove",
        "come_accedere",
        "orari_apertura",
        "contatti",
        "servizi",
        "persone_struttura",
        "contenuti_collegati",
        "ulteriori_informazioni",
        "settings",
        "ownership",
        "dates",
        "categorization",
        "seo",
    ],
    "News Item": [
        "default",
        "dates",
        "contenuti_collegati",
        "categorization",
        "settings",
        "ownership",
    ],
    "Persona": [
        "default",
        "ruolo",
        "dove",
        "contatti",
        "ulteriori_informazioni",
        "categorization",
        "dates",
        "ownership",
        "settings",
    ],
    "PuntoDiContatto": [
        "default",
    ],
    "Servizio": [
        "default",
        "cose",
        "a_chi_si_rivolge",
        "accedi_al_servizio",
        "cosa_serve",
        "costi_e_vincoli",
        "tempi_e_scadenze",
        "casi_particolari",
        "contatti",
        "documenti",
        "link_utili",
        "ulteriori_informazioni",
        "contenuti_collegati",
        "categorization",
        "settings",
        "ownership",
        "dates",
    ],
    "UnitaOrganizzativa": [
        "default",
        "cosa_fa",
        "struttura",
        "persone",
        "contatti",
        "contenuti_collegati",
        "categorization",
        "ulteriori_informazioni",
        "settings",
        "ownership",
        "dates",
    ],
    "Venue": [
        "default",
        "descrizione",
        "accesso",
        "dove",
        "orari",
        "contatti",
        "ulteriori_informazioni",
        "settings",
        "contenuti_collegati",
        "categorization",
    ],
}


@implementer(IPublishTraverse)
class TypesGet(BaseGet):
    def customize_versioning_fields_fieldset(self, result):
        """
        Unico modo per spostare i campi del versioning.
        Perché changeNotes ha l'order after="*" che vince su tutto.
        """
        versioning_fields = ["versioning_enabled", "changeNote"]
        for field in versioning_fields:
            found = False
            for fieldset in result["fieldsets"]:
                if fieldset.get("id") == "default" and field in fieldset["fields"]:
                    found = True
                    fieldset["fields"].remove(field)
                if fieldset.get("id") == "settings" and found:
                    fieldset["fields"].append(field)

        return result

    def customize_servizio_schema(self, result):
        result.get("required").append("description")
        return result

    def customize_evento_schema(self, result):
        result.get("required").append("description")
        return result

    def customize_uo_schema(self, result):
        result.get("required").append("description")
        versioning_fields = ["contact_info"]
        for field in versioning_fields:
            for fieldset in result["fieldsets"]:
                if fieldset.get("id") == "contatti" and field in fieldset["fields"]:
                    fieldset["fields"].remove(field)
                    fieldset["fields"].insert(0, field)
        return result

    def customize_news_schema(self, result):
        result.get("required").append("description")
        if self.context.portal_type == "News Item":
            # we are in a news and not in container
            review_state = self.context.portal_workflow.getInfoFor(
                self.context, "review_state"
            )
            if review_state == "published":
                result.get("required").append("effective")

        return result

    def customize_documento_schema(self, result):
        result.get("required").append("description")
        return result

    def reply(self):
        result = super(TypesGet, self).reply()
        if "fieldsets" in result:
            result["fieldsets"] = self.reorder_fieldsets(schema=result)
        pt = self.request.PATH_INFO.split("/")[-1]

        # be careful: result could be dict or list. If list it will not
        # contains title. And this is ok for us.
        pt = self.request.PATH_INFO.split("/")[-1]

        if "title" in result:
            if pt == "Persona":
                result = self.customize_persona_schema(result)
            # if pt == "Venue":
            #     result = self.customize_venue_schema(result)
            if pt == "Document":
                result = self.customize_document_schema(result)
            if pt == "Servizio":
                result = self.customize_servizio_schema(result)
            if pt == "UnitaOrganizzativa":
                result = self.customize_uo_schema(result)
            if pt == "News Item":
                result = self.customize_news_schema(result)
            if pt == "Documento":
                result = self.customize_documento_schema(result)
            if pt == "Event":
                result = self.customize_evento_schema(result)
            result = self.customize_versioning_fields_fieldset(result)
        return result

    def get_order_by_type(self, portal_type):
        return [x for x in FIELDSETS_ORDER.get(portal_type, [])]

    def reorder_fieldsets(self, schema):
        original = schema["fieldsets"]
        pt = self.request.PATH_INFO.split("/")[-1]
        order = self.get_order_by_type(portal_type=pt)
        if not order:
            # no match
            return original
        original_fieldsets = [x["id"] for x in original]
        for fieldset_id in original_fieldsets:
            # if some fieldsets comes from additional addons (not from the
            # base ones), then append them to the order list.
            if fieldset_id not in order:
                order.append(fieldset_id)

        # create a new fieldsets list with the custom order
        new = []
        for id in order:
            for fieldset in original:
                if fieldset["id"] == id and self.fieldset_has_fields(fieldset, schema):
                    new.append(fieldset)
        if not new:
            # no match
            return original
        return new

    def fieldset_has_fields(self, fieldset, schema):
        """
        If a fieldset has all hidden fields (maybe after a schema tweak),
        these are not in the schema data, but are still in fieldset data.
        This happens only in add, because the schema is generate with the parent's context.
        """
        fieldset_fields = fieldset["fields"]

        schema_fields = [x for x in fieldset_fields if x in schema["properties"].keys()]

        return len(schema_fields) > 0
