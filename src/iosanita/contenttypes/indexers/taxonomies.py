# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from collective.taxonomy import PATH_SEPARATOR
from collective.taxonomy.interfaces import ITaxonomy
from zope.component import getUtility
from zope.globalrequest import getRequest
from plone.dexterity.interfaces import IDexterityContent


def extract_taxonomies(context, field):
    request = getRequest()
    taxonomy = getUtility(ITaxonomy, name=f"collective.taxonomy.{field}")
    taxonomy_voc = taxonomy.makeVocabulary(request.get("LANGUAGE"))
    data = []
    for key in getattr(context, field, []) or []:
        value = taxonomy_voc.inv_data.get(key, None)

        if not value:
            continue
        if value.startswith(PATH_SEPARATOR):
            value = value.replace(PATH_SEPARATOR, "", 1)
        data.append({"title": value.replace(PATH_SEPARATOR, "", 1), "token": key})
    return data


@indexer(IDexterityContent)
def parliamo_di_metadata(context, **kw):
    """ """
    return extract_taxonomies(context=context, field="parliamo_di")


@indexer(IDexterityContent)
def a_chi_si_rivolge_tassonomia_metadata(context, **kw):
    """ """
    return extract_taxonomies(context=context, field="a_chi_si_rivolge_tassonomia")
