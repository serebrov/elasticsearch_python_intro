import os
import json

from elasticsearch import Elasticsearch, helpers as es_helpers
from elasticsearch.exceptions import NotFoundError
import settings
from helpers import geo_csv


def recreate_index():
    es = Elasticsearch([settings.ES_URL])
    try:
        es.indices.delete(index=settings.ES_INDEX)
    except NotFoundError:
        pass
    es.indices.create(index=settings.ES_INDEX, body=settings.index_settings)
    return es


def load_data(es):
    # Load countries.
    file_name = os.path.join('data', 'countryInfo.txt')
    countries = geo_csv.get_countries(file_name)
    save_geo_data(es, countries, 'countries')

    # Load cities.
    file_name = os.path.join('data', 'cities15000.txt')
    cities = geo_csv.get_geo_objects(file_name)
    save_geo_data(es, cities, 'geo-objects')

    # Load points of interest.
    file_name = os.path.join('data', 'geoObjects.txt')
    geo_objects = geo_csv.get_geo_objects(file_name)
    save_geo_data(es, geo_objects, 'geo-objects')


def save_geo_data(es, data, data_type):
    bulk_data = []
    for item in data:
        bulk_data.append({
            '_index': settings.ES_INDEX,
            '_id': str(item['geonameid']),
            '_type': data_type,
            '_source': json.dumps(item),
        })
        if len(bulk_data) % 1000 == 0:
            es_helpers.bulk(es, bulk_data)
            bulk_data = []
    es_helpers.bulk(es, bulk_data)

    # Single doc example:
    #
    # es.index(
    #     index=ES_INDEX,
    #     doc_type='countries',
    #     id=str(item['geonameid']),
    #     body=json.dupms(item),
    # )


def main():
    es = recreate_index()
    load_data(es)


if __name__ == '__main__':
    main()
