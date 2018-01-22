The simple ElasticSearch 5 example in python: we load countries data into the ElasticSearch and then query the data by text.

## Installation

* Clone the repo
* Run `./install.sh` to create virtual environment and install requirements
* Run `venv/bin/activate` to activate the virtual environment

## Usage

1. Prepare the data, run `./data/get-data.sh`.
The script will download the geo objects csv from geonames.org and filter out the subset of full data.

2. Run the ElasticSearch using `./run.sh`. It will download ElasticSearch if necessary.

3. Load the data using `python load-data.py`.
It will read the [countryInfo.txt](./data/countryInfo.txt) data into the running ElasticSearch.

The data is downloaded from the http://www.geonames.org/ and contains the list of countries with related data (capital, currency, area, population, etc).

4. Search the data using `python search-by-text.py query`, where "query" is the text to search for, which can be a part of country or capital name, currency name or code.

Example:

```text
(venv) $ python search-by-text.py eur
Germany, capital: Berlin, currency: Euro
France, capital: Paris, currency: Euro
Italy, capital: Rome, currency: Euro
Spain, capital: Madrid, currency: Euro
Netherlands, capital: Amsterdam, currency: Euro
Greece, capital: Athens, currency: Euro
Portugal, capital: Lisbon, currency: Euro
Belgium, capital: Brussels, currency: Euro
Austria, capital: Vienna, currency: Euro
Slovakia, capital: Bratislava, currency: Euro
Finland, capital: Helsinki, currency: Euro
Ireland, capital: Dublin, currency: Euro
Lithuania, capital: Vilnius, currency: Euro
Latvia, capital: Riga, currency: Euro
Slovenia, capital: Ljubljana, currency: Euro
Kosovo, capital: Pristina, currency: Euro
Estonia, capital: Tallinn, currency: Euro
Cyprus, capital: Nicosia, currency: Euro
Reunion, capital: Saint-Denis, currency: Euro
Montenegro, capital: Podgorica, currency: Euro
```

5. Search by geo location using `python search-by-geo-location.py {longitude} {latitude}`.

For example (London):

```text
(venv) $ python search-by-geo-location.py 51.51 -0.13
(geo-objects) London Dungeon, type: S.MUS, positing: 51.5027,-0.1194
(geo-objects) Sherlock Holmes Museum, type: S.MUS, positing: 51.52378,-0.15856
(geo-objects) Monument to the Great Fire of London, type: S.MNMT, positing: 51.51014,-0.08594
(geo-objects) The View from the Shard, type: S.OBPT, positing: 51.50449,-0.08691
(geo-objects) Ripley's Believe It Or Not!, type: S.MUS, positing: 51.51018,-0.13386
(geo-objects) The Serpentine, type: H.PND, positing: 51.50524,-0.16643
(geo-objects) Churchill War Rooms, type: S.MUS, positing: 51.50186,-0.12912
(geo-objects) Nelson's Column, type: S.MNMT, positing: 51.50777,-0.12792
(geo-objects) Kennington Park, type: L.PRK, positing: 51.48423,-0.10865
(geo-objects) Round Pond, type: H.PND, positing: 51.506,-0.18317
(geo-objects) The Long Water, type: H.PND, positing: 51.50954,-0.17527
(geo-objects) The Royal Parks, type: L.PRK, positing: 51.50828,-0.1652
(geo-objects) Kensington Palace Green, type: L.PRK, positing: 51.5041,-0.18905
...
```

## Reference

[ElasticSearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)

[Python Client Documentation](http://elasticsearch-py.readthedocs.io/en/master/api.html)
