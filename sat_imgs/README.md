# Drone Imagery
Road condition detection using drones

## Getting the Road Points
File : `roadPoints.py`

Requesting the [overpass](http://overpass-api.de/) API from OSM, you can download a set of points between set of coordinates 
called a bounding box (this can also be a polygon). 

We use the [highway keyword](http://wiki.openstreetmap.org/wiki/Key:highway) and download the type of road we want from the tile 
that was selected before. Only highway=motorway/motorway_link implies anything about quality. 

This request creates a csv file with a set of lat, long points.

## Getting the dataset
File : `imgDownload.py`

To get the images, you need to get a Google Maps API [secret key](https://developers.google.com/maps/documentation/directions/get-api-key) and a Google Street View [secret key](https://developers.google.com/maps/documentation/streetview/)
and send them as parameters to the script.

The above command assumes that the keys as set as temp environment variables.

This script will create a list of urls based on the points that come from the csv file that contains the latitud and longitud 
points. From this url list it will get the images and save them as png files.

## To Run the Script

The following instructions assume you get the secret keys from environmental variables, the first one is for stellite 
the second for street view

Good satellite data:
`python imgDownload.py $gKey $svKey satellite_good 0 points/location_points_good.csv`

Bad satellite data:
`python imgDownload.py $gKey $svKey satellite_bad 0 points/location_points_bad.csv`

### Type changes to 1 (see script for description of params)

Good street_view data:
`python imgDownload.py $gKey $svKey sv_good 1 points/location_points_good.csv`

Bad street_view data:
`python imgDownload.py $gKey $svKey sv_bad 1 points/location_points_bad.csv`