import csv
# import unicodecsv


country_fieldnames = [
    'iso', 'iso3', 'iso_numeric', 'fips', 'name',
    'capital', 'area', 'population', 'continent',
    'tld', 'currency_code', 'currency_name',
    'phone', 'postal_code_format', 'postal_code_regex',
    'languages', 'geonameid', 'neighbours',
    'equivalent_fips_code'
]

geo_fieldnames = [
    'geonameid',         # : integer id of record in geonames database
    'name',              # : name of geographical point (utf8) varchar(200)
    'asciiname',         # : name of geographical point in plain ascii characters, varchar(200)
    'alternatenames',    # : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
    'latitude',          # : latitude in decimal degrees (wgs84)
    'longitude',         # : longitude in decimal degrees (wgs84)
    'feature_class',     # : see http://www.geonames.org/export/codes.html, char(1)
    'feature_code',      # : see http://www.geonames.org/export/codes.html, varchar(10)
    'country_code',      # : ISO-3166 2-letter country code, 2 characters
    'cc2',               # : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
    'admin1_code',       # : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
    'admin2_code',       # : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
    'admin3_code',       # : code for third level administrative division, varchar(20)
    'admin4_code',       # : code for fourth level administrative division, varchar(20)
    'population',        # : bigint (8 byte int)
    'elevation',         # : in meters, integer
    'dem',               # : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
    'timezone',          # : the iana timezone id (see file timeZone.txt) varchar(40)
    'modification_date'  # : date of last modification in yyyy-MM-dd format
]


def get_countries(file_name):
    data = read_file(file_name, country_fieldnames)
    for row in data:
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


def get_geo_objects(file_name):
    data = read_file(file_name, geo_fieldnames)
    for row in data:
        context = {
            '_type': ['all', 'points-of-interest'],
        }
        row['_suggest'] = {
            'contexts': context,
            'input': prepare_suggester_input([
                row['name'],
                row['alternatenames'],
            ]),
            'weight': row['population'],
        }
        row['geoLocation'] = {
            'latitude': row['latitude'],
            'longitude': row['longitude']
        }
        row['geoPoint'] = {
            'location': {
                'lat': float(row['latitude']),
                'lon': float(row['longitude']),
            }
        }
        # row['geoViewport'] = {
        #     'northeast': {
        #         'latitude': self.viewport_northeast_latitude,
        #         'longitude': self.viewport_northeast_longitude,
        #     },
        #     'southwest': {
        #         'latitude': self.viewport_southwest_latitude,
        #         'longitude': self.viewport_southwest_longitude,
        #     },
        # }
        yield row


def read_file(file_name, fieldnames):
    with open(file_name) as csv_file:
        # See the list of fields in the countryInfo.txt
        reader = csv.DictReader(
            (line for line in csv_file if not line.startswith('#')),
            fieldnames=fieldnames,
            # geodata files sometimes contain quote chars in names, like:
            # 6615476	...	"ujuk Dzhamja,Buyuk Dzhamya,...
            # by default this is being interpreted as multi-line field, so
            # we need to disable quoting:
            quoting=csv.QUOTE_NONE,
            dialect='excel-tab')  # , encoding='utf-8')

        for row in reader:
            yield row


def prepare_suggester_input(inputs):
    result = []
    for item in inputs:
        if item:
            result.append(item)
    return result
