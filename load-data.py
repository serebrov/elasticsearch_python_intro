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
            '_type': 'countries',
            '_source': json.dumps(item),
        })
    es_helpers.bulk(es, data)

    # Single doc example:
    #
    # es.index(
    #     index=ES_INDEX,
    #     doc_type='countries',
    #     id=str(item['geonameid']),
    #     body=json.dupms(item),
    # )


def prepare_suggester_input(inputs):
    result = []
    for item in inputs:
        if item:
            result.append(item)
    return result


def get_countries():
    file_name = os.path.join('data', 'countryInfo.txt')
    with open(file_name) as csv_file:
        # See the list of fields in the countryInfo.txt
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
            context = {
                '_type': ['all', 'countries'],
            }
            row['_suggest'] = {
                'contexts': context,
                'input': prepare_suggester_input([
                    row['name'],
                    row['capital'],
                    row['currency_name'],
                    row['currency_code'],
                ]),
                'weight': row['population'],
            }
            yield row


def main():
    es = recreate_index()
    load_data(es)


if __name__ == '__main__':
    main()
