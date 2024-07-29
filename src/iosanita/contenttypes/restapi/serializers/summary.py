from plone.restapi.interfaces import IJSONSummarySerializerMetadata
from zope.interface import implementer


@implementer(IJSONSummarySerializerMetadata)
class JSONSummarySerializerMetadata:
    def default_metadata_fields(self):
        """
        Force always return some metadata
        """
        return {"parliamo_di_metadata", "a_chi_si_rivolge_tassonomia_metadata", "id"}
