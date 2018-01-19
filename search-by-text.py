import argparse
from elasticsearch import Elasticsearch
import settings


def search_text(es, index, query):

    # We could make it configurable and allow selecting the document
    # type to search
    _type = ['countries', 'geo-objects']

    # Suggester will search through all data we put into 'suggest'
    query = {
        "suggest": {
            "suggestions": {
                "text": query,
                "completion": {
                    "context": {
                        "_type": _type,
                    },
                    "field": "_suggest",
                    "size": 20,
                    "fuzzy": {
                        "fuzziness": 1,
                        "min_length": 5,
                    },
                },
            },
        },
    }

    result = es.search(
        body=query,
        index=index,
    )

    suggest = result['suggest']
    suggestions = suggest.get('suggestions', [])
    for suggestion in suggestions:
        options = suggestion.get('options')
        for i, option in enumerate(options):
            item = option['_source']
            yield item


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search data by text query')
    parser.add_argument('query', metavar='query')
    args = parser.parse_args()

    es = Elasticsearch([settings.ES_URL])
    results = search_text(es, settings.ES_INDEX, args.query)
    for r in results:
        if r['type'] == 'countries':
            print('({type}) {name}, capital: {capital}, currency: {currency_name}'.format(**r))
        else:
            print('({type}) {name}, type: {feature_class}.{feature_code}, positing: {latitude},{longitude}'.format(**r))
