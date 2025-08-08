from iosanita.contenttypes.interfaces import IoSanitaViewExtraData
from iosanita.contenttypes.restapi.services.view_extra_data.extractor import (
    ViewExtraDataExtractor,
)
from irst.policy.content.at import IAT
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IoSanitaViewExtraData)
@adapter(IAT, Interface)
class ViewExtraDataExtractorAT(ViewExtraDataExtractor):
    def __call__(self):
        bando_view = self.context.restrictedTraverse("bando_view")
        return {
            # "approfondimenti": self.get_approfondimenti(),
            "stato_bando": bando_view.getBandoState(),
        }
