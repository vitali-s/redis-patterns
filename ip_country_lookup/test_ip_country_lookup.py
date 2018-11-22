import redis
import csv
import os
import json

connection = redis.Redis(host='127.0.0.1', port=6379, db=0)

KEY_IP_TO_CITY = 'ip2city:'
KEY_CITY_LOOKUP = 'cityid2city:'

def test_ip_country_lookup():
    # load data
    #filepath = os.path.join(os.path.dirname(__file__), 'GeoLiteCity-Blocks.csv')
    #import_ips_to_redis(filepath)

    # load data
    #cities_filepath = os.path.join(os.path.dirname(__file__), 'GeoLiteCity-Location.csv')
    #import_cities_to_redis(cities_filepath)

    city = find_city_by_ip('123.10.1.13')

    assert city[0] == 'Dearborn' and city[1] == 'MI' and city[2] == 'US'
    


def ip_to_score(ip_address):
    score = 0

    for v in ip_address.split('.'):
        score = score * 265 + int(v, 10)

    return score


def import_ips_to_redis(filename):
    connection.delete(KEY_IP_TO_CITY)

    csv_file = csv.reader(open(filename, 'rt', encoding = 'utf8'))

    for count, row in enumerate(csv_file):
        start_ip = row[0] if row else ''

        if 'i' in start_ip.lower():
            continue
        if '.' in start_ip:
            start_ip = ip_to_score(start_ip)
        elif start_ip.isdigit():
            start_ip = int(start_ip, 10)
        else:
            continue

        city_id = row[2] + '_' + str(count)

        connection.zadd(KEY_IP_TO_CITY, { city_id: start_ip })

def import_cities_to_redis(filename):
    connection.delete(KEY_CITY_LOOKUP)

    csv_file = csv.reader(open(filename, 'rt', encoding = 'utf8'))

    for row in csv_file:
        if len(row) < 4 or not row[0].isdigit():
            continue

        city_id = row[0]
        country = row[1]
        region = row[2]
        city = row[3]

        connection.hset(KEY_CITY_LOOKUP, city_id, json.dumps([city, region, country]))

def find_city_by_ip(ip_address):
    if isinstance(ip_address, str):
        ip_address = ip_to_score(ip_address)

    city_id = connection.zrevrangebyscore(KEY_IP_TO_CITY, ip_address, 0, start = 0, num = 1)

    if not city_id:
        return None

    city_id = city_id[0].decode().partition('_')[0]

    data = connection.hget(KEY_CITY_LOOKUP, city_id)

    if data is not None:
        return json.loads(data)

    return ''