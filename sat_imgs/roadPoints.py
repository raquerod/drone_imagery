#http://127.0.0.1:5000/{service}/{version}/{profile}/{coordinates}[.{format}]?option=value&option=value
#'http://router.project-osrm.org/nearest/v1/driving/13.388860,52.517037?number=3&bearings=0,20'
#'http://router.project-osrm.org/route/v1/driving/13.388860,52.517037;13.397634,52.529407;13.428555,52.523219?overview=false'

import requests

r = requests.get('http://www.overpass-api.de/api/data=[out:json]?node[bbox=68.11,20.12,74.48,24.71][highway=primary]')
