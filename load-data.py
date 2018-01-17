import os
import json
import csv
# import unicodecsv

from elasticsearch import Elasticsearch, helpers as es_helpers
import settings


def recreate_index():
    es = Elasticsearch([settings.ES_URL])
    es.indices.delete(index=settings.ES_INDEX)
    es.indices.create(index=settings.ES_INDEX, body=settings.index_settings)
    return es


def load_data(es):
    data = []
    countries = get_countries()
    for item in countries:
        data.append({
            '_index': settings.ES_INDEX,
            '_id': str(item['geonameid']),
            '_type': 'country',
            '_source': json.dumps(item),
        })
    es_helpers.bulk(es, data)

    # Single doc example:
    #
    # es.index(
    #     index=ES_INDEX,
    #     doc_type='country',
    #     id=str(item['geonameid']),
    #     body=json.dupms(item),
    # )
    # ans = True


def get_countries():
    file_name = os.path.join('data', 'countryInfo.txt')
    with open(file_name) as csv_file:
        fieldnames = [
            'iso', 'iso3', 'iso_numeric', 'fips', 'name',
            'capital', 'area', 'population', 'continent',
            'tld', 'currency_code', 'currency_name',
            'phone', 'postal_code_format', 'postal_code_regex',
            'languages', 'geonameid', 'neighbours',
            'equivalent_fips_code'
        ]
        reader = csv.DictReader(
            (line for line in csv_file if not line.startswith('#')),
            fieldnames=fieldnames,
            dialect='excel-tab')  # , encoding='utf-8')

        for row in reader:
            yield row


def main():
    es = recreate_index()
    load_data(es)


if __name__ == '__main__':
    main()
