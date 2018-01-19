ES_INDEX = 'geo_data'
ES_URL = 'http://127.0.0.1:9200'


# Mappings define the filed types, so they can be properly indexed and searched
# See: https://www.elastic.co/guide/en/elasticsearch/reference/6.1/mapping-types.html
#
# Note: ElasticSearch 6 also announced removal of mapping types,
# see https://www.elastic.co/guide/en/elasticsearch/reference/6.1/removal-of-types.html
#     https://www.elastic.co/blog/kibana-6-removal-of-mapping-types
# We can have unified structure, with one document type "geoobject", where the specific
# data is stored in the 'city' / 'country', 'point-of-interest' sub-object.

# Completion suggester,
# see https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters-completion.html
_suggest_mapping = {
    'type': 'completion',
    'analyzer': 'default',
    'preserve_separators': False,
    'preserve_position_increments': True,
    'max_input_length': 50,
    'contexts': [{
        'name': '_type',
        'type': 'category'
    }]
}


geo_location_maping = {
    'properties': {
        'latitude': {'index': 'not_analyzed', 'type': 'double'},
        'longitude': {'index': 'not_analyzed', 'type': 'double'},
    },
}


geo_point_mapping = {
    'properties': {
        'location': {'type': 'geo_point'},
    },
}


geo_viewport_mapping = {
    'properties': {
        'northeast': {
            'properties': {
                'latitude': {'index': 'not_analyzed', 'type': 'double'},
                'longitude': {'index': 'not_analyzed', 'type': 'double'},
            },
        },
        'southwest': {
            'properties': {
                'latitude': {'index': 'not_analyzed', 'type': 'double'},
                'longitude': {'index': 'not_analyzed', 'type': 'double'},
            },
        },
    },
}


country_mapping = {
    'properties': {
        'name': {'index': 'not_analyzed', 'type': 'string'},
        'isoCode': {'index': 'not_analyzed', 'type': 'string'},
    },
}


mappings = {
    'countries': {
        'properties': {
            '_suggest': _suggest_mapping,
            'type': {'type': 'keyword'},
            'geonameid': {'type': 'keyword'},
            # 'geoLocation': geo_location_maping,
            # 'geoPoint': geo_point_mapping,
            # 'geoViewport': geo_viewport_mapping,
            'name': {'type': 'string'},
            'currency_code': {'type': 'string'},
            'currency_name': {'type': 'string'},
            'languages': {'type': 'string'},
            'area': {'type': 'double'},
            'population': {'type': 'integer'},
            'iso': {'index': 'not_analyzed', 'type': 'string'},
        },
    },
    'geo-objects': {
        'properties': {
            '_suggest': _suggest_mapping,
            'type': {'type': 'keyword'},
            'geonameid': {'type': 'keyword'},
            'name': {'type': 'string'},
            'feature_class': {'type': 'string'},
            'feature_code': {'type': 'string'},
            'country_code': {'type': 'string'},
            'population': {'type': 'integer'},
            'geoLocation': geo_location_maping,
            'geoPoint': geo_point_mapping,
            'geoViewport': geo_viewport_mapping,
        },
    },
}

index_settings = {
    'settings': {
        'index': {
            'number_of_replicas': '1',
            'number_of_shards': '3',
            'analysis': {
                'analyzer': {
                    'default': {
                        'tokenizer': 'icu_tokenizer',
                        'filter': [
                            'icu_folding',
                            'icu_normalizer',
                        ],
                    },
                },
            },
        },
    },
    'mappings': mappings
}
