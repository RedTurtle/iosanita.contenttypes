from collective.taxonomy import PATH_SEPARATOR
from iosanita.contenttypes.indexers.taxonomies import get_taxonomy_vocab
from iosanita.contenttypes.interfaces import IIosanitaContenttypesLayer
from plone.restapi.interfaces import IJSONSummarySerializerMetadata
from plone.restapi.interfaces import ISerializeToJsonSummary
from redturtle.volto.restapi.serializer.summary import DefaultJSONSummarySerializer
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IJSONSummarySerializerMetadata)
class JSONSummarySerializerMetadata:
    def default_metadata_fields(self):
        """
        Force always return some metadata
        """
        return {
            "parliamo_di_metadata",
            "a_chi_si_rivolge_tassonomia_metadata",
            "id",
            "tipologia_notizia",
        }


@implementer(ISerializeToJsonSummary)
@adapter(Interface, IIosanitaContenttypesLayer)
class IOSanitaJSONSummarySerializer(DefaultJSONSummarySerializer):
    def __call__(self):
        """
        Customize type_title for News Items
        """
        data = super().__call__()

        if data["@type"] != "News Item":
            return data
        tipologia_notizia = getattr(self.context, "tipologia_notizia")
        if tipologia_notizia:
            tipologia_notizia = tipologia_notizia[0]
            taxonomy_vocab = get_taxonomy_vocab("tipologia_notizia")
            taxonomy_value = taxonomy_vocab.inv_data.get(tipologia_notizia, None)
            if taxonomy_value:
                data["type_title"] = taxonomy_value.replace(PATH_SEPARATOR, "", 1)
            else:
                data["type_title"] = "Notizia"
        else:
            data["type_title"] = "Notizia"
        return data
