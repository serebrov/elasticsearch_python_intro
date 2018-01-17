The simple ElasticSearch 5 example in python: we load countries data into the ElasticSearch and then query the data by text.

## Installation

* Clone the repo
* Run `./install.sh` to create virtual environment and install requirements
* Run `venv/bin/activate` to activate the virtual environment

## Usage

1. Run the ElasticSearch using `./run.sh`. It will download ElasticSearch if necessary.

2. Load the data using `python load-data.py`.
It will read the [countryInfo.txt](./data/countryInfo.txt) data into the running ElasticSearch.

The data is downloaded from the http://www.geonames.org/ and contains the list of countries with related data (capital, currency, area, population, etc).

3. Search the data using `python search-by-text.py query`, where "query" is the text to search for, which can be a part of country or capital name, currency name or code.

## Reference

[ElasticSearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)

[Python Client Documentation](http://elasticsearch-py.readthedocs.io/en/master/api.html)
