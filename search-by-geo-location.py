import argparse
from elasticsearch import Elasticsearch
import settings

# Kiev:
#   python search-by-geo-location.py 50.53 30.46
# London:
#   python search-by-geo-location.py 51.51 -0.13


def search_geo(es, index, latitude, longitude):

    search_delta = 0.1
    _type = ['geo-objects']

    # We search using "geo_bounding_box" query:
    # https://www.elastic.co/guide/en/elasticsearch/guide/1.x/geo-bounding-box.html
    # It expects top-left and bottom-right coordinates, while we have
    # top-right (northeast) and bottom-left (southwest)
    # So we exchange the longitude coordinates before search:
    #
    #                   North
    #
    #           Top-Left (North-West)
    #               x--------------
    #            ^  |             |
    # West       |  |             |    East
    #          +Lat |  +Long-->   |
    #               o-------------x
    #                         Bottom-Right (South-East)
    #
    #                    South
    #
    top_left_lat = latitude + search_delta
    top_left_lon = longitude - search_delta
    bottom_right_lat = latitude - search_delta
    bottom_right_lon = longitude + search_delta

    query = {
        "query": {
            "bool": {
                "filter": [
                    {"geo_bounding_box": {
                        "geoPoint.location": {
                            "top_left": {
                                "lat":  top_left_lat,
                                "lon": top_left_lon
                            },
                            "bottom_right": {
                                "lat":  bottom_right_lat,
                                "lon": bottom_right_lon,
                            }
                        }
                    }},
                ]
            },
        },
        "sort": {
            "population": {
                "order": "asc",
                "missing": "_last",
            },
            "geonameid": {
                "order": "asc",  # To make sorting stable
            },
        },
    }

    result = es.search(
        index=index,
        doc_type=_type,
        body=query,
        size=50,
    )
    hits = result['hits']['hits']

    for i, hit in enumerate(hits):
        yield hit['_source']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search data by geo location ("near me")')
    parser.add_argument('longitude', metavar='longitude')
    parser.add_argument('latitude', metavar='latitude')
    args = parser.parse_args()

    es = Elasticsearch([settings.ES_URL])
    results = search_geo(
        es,
        settings.ES_INDEX,
        # todo: setup floats for arg parser
        float(args.longitude),
        float(args.latitude))
    for r in results:
        if r['type'] == 'countries':
            print('({type}) {name}, capital: {capital}, currency: {currency_name}'.format(**r))
        else:
            print('({type}) {name}, type: {feature_class}.{feature_code}, positing: {latitude},{longitude}'.format(**r))
