from plone.restapi.interfaces import ISerializeToJson
from zope.interface import implementer
from plone.volto.interfaces import IFolderishNewsItem
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from iosanita.contenttypes.interfaces import IIosanitaContenttypesLayer
from zope.component import adapter
from iosanita.contenttypes.indexers.taxonomies import get_taxonomy_vocab
from collective.taxonomy import PATH_SEPARATOR


@implementer(ISerializeToJson)
@adapter(IFolderishNewsItem, IIosanitaContenttypesLayer)
class NewsItemSerializeToJson(SerializeFolderToJson):

    def __call__(self, version=None, include_items=True):
        data = super().__call__(version=version, include_items=include_items)

        tipologia_notizia = getattr(self.context, "tipologia_notizia")
        taxonomy_vocab = get_taxonomy_vocab("tipologia_notizia")
        taxonomy_value = taxonomy_vocab.inv_data.get(tipologia_notizia, None)
        if taxonomy_value:
            data["type_title"] = taxonomy_value.replace(PATH_SEPARATOR, "", 1)
        else:
            data["type_title"] = "Notizia"
        return data
