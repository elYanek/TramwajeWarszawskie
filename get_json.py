# -*- coding: utf-8 -*-

from urllib.request import urlopen
import datetime
import json
import database_access

# user_key = u''
# api_id = ''
# adress = r'https://api.um.warszawa.pl/api/action/wsstore_get/?id={0}&apikey={1}'
# url = adress.format(api_id,user_key)

def transform_data(tram_dictionary):
    fields = ('Brigade', 'FirstLine', 'Lines', 'Status', 'Time', 'Lon', 'Lat', 'LowFloor')

    translate_fields = {
        'Brigade':'brigade',
        'FirstLine' : 'first_line',
        'Lines':'lines',
        'Status':'status',
        'Time':'time',
        'Lon':'lon',
        'Lat':'lat',
        'LowFloor':'low_floor'
    }

    converted_tram_dict = {}

    date_format = "%Y-%m-%dT%H:%M:%S"

    brigade = "'{0}'".format(str(tram_dictionary[fields[0]]).replace(' ',''))
    first_line = "'{0}'".format(str(tram_dictionary[fields[1]]).replace(' ',''))
    lines = "'{0}'".format(str(tram_dictionary[fields[2]]).replace(' ',''))
    status = "'{0}'".format(str(tram_dictionary[fields[3]]).replace(' ',''))
    date = "'{0}'".format(datetime.datetime.strptime(tram_dictionary[fields[4]], date_format))
    lon = str(tram_dictionary[fields[5]])
    lat = str(tram_dictionary[fields[6]])
    low_floor = str(tram_dictionary[fields[7]])

    converted_tram_dict[translate_fields[fields[0]]] = brigade
    converted_tram_dict[translate_fields[fields[1]]] = first_line
    converted_tram_dict[translate_fields[fields[2]]] = lines
    converted_tram_dict[translate_fields[fields[3]]] = status
    converted_tram_dict[translate_fields[fields[4]]] = date
    converted_tram_dict[translate_fields[fields[5]]] = lon
    converted_tram_dict[translate_fields[fields[6]]] = lat
    converted_tram_dict[translate_fields[fields[7]]] = low_floor

    return converted_tram_dict


def main():
    url = 'https://api.um.warszawa.pl/api/action/wsstore_get/?' \
          'id=c7238cfe-8b1f-4c38-bb4a-de386db7e776&' \
          'apikey=c67f064e-90ed-4bea-bd92-686ab39eb916'
    # print(url)

    u = urlopen(url).read().decode("utf-8")

    rest = json.loads(u)

    trams = rest['result']

    conn = database_access.DbConnection()

    process_data = datetime.datetime.now()

    x = 1

    for tram in trams:
        # print(x)

        converted_dict = transform_data(tram)
        converted_dict['proc_date'] = "'{0}'".format(str(process_data))

        pt1 = converted_dict['lon']
        pt2 = converted_dict['lat']

        converted_dict['geom'] = '({0})'.format(conn.insert_point([pt1, pt2], 4326))
        # print(converted_dict)

        conn.add_values_from_dict('tramwaje_lokalizacja', converted_dict)

        x += 1

    print("Added {0} records.".format(len(trams)))

    conn.clear_values_by_time('tramwaje_lokalizacja', 'proc_date', 60)

    conn.close_db_comminucation()
