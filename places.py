#!/usr/bin/env python
# -*- coding: utf-8 -*-
import googlemaps
import codecs
import json
import re

# Get awesome working places from README.md
search_results = []
print 'Parsing results from README.md...'
with codecs.open('README.md', 'r', 'utf-8') as fp:
    for line in fp:
        if re.search("^#", line):
            if not 'workplaces' in line:
                if not 'Cities' in line:
                    if not 'Contributors' in line:
                        search_results.append(line)
# Prettify results
city = ''
places = []
print 'Prettifying results...'
for item in search_results:
    if item.count('#') == 1:
        city = item.strip('#').strip()
        continue
    item = item.strip('#').strip()
    place = {'city': city, 'name': item}
    places.append(place)

# Geocode each place
gmaps = googlemaps.Client(key='API_KEY')

results = []
for place in places:
    geocoding_string = place['name'] + ', ' + place['city'] + ', Slovenia'
    print 'Geocoding:' + geocoding_string

    geocode_result = gmaps.geocode(
        geocoding_string)
    if(geocode_result):
        geo = geocode_result[0]['geometry']['location']
        result = {}
        result['placeName'] = place['name']
        result['lat'] = geo['lat']
        result['lng'] = geo['lng']
        result['address'] = geocode_result[0]['formatted_address']
        results.append(result)
    else:
        print 'No data found for ' + geocoding_string

# Write results to file
print 'Writing results to file...'
with codecs.open('places.json', 'w', 'utf-8') as f:
    f.write(json.dumps(results, sort_keys=True, ensure_ascii=False))
