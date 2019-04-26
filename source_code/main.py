import json
import folium
import overpy
import logging
from constants import RADIUS, TAG, QUERY_TEMPLATE, NTH_POINT, OUTPUT_FILE

logging.getLogger().setLevel(logging.INFO)

logging.info("Creating Overpass api handler")

api = overpy.Overpass()

logging.info("Creating Overpass api handler - Finished")
logging.info("Load geojson data")

with open('route.geojson', encoding='utf-8') as geojson:
    data = json.load(geojson)
    geometry = data.get('geometry')

    logging.info("Load geojson data - Finished")

# coordinates in route file are stored in (latitude, longitude) order
# it must be swapped
coordinates = []
for lat, lon in geometry.get('coordinates'):
    coordinates.append((lon, lat))

# calculate the middle point when the map loads
middle_idx = len(coordinates) // 2
center = coordinates[middle_idx]


logging.info("Create map")

# create a map pointing at middle route with initial zoom of 6
my_map = folium.Map(location=center, zoom_start=6)
folium.PolyLine(coordinates).add_to(my_map)

logging.info("Map created")

logging.info("Query point of intrest for tag {TAG}".format(TAG=TAG))

for latitude, longitude in coordinates[::NTH_POINT]:
    result = api.query(
        QUERY_TEMPLATE.format(
            tag=TAG, radius=RADIUS, lat=latitude, lon=longitude
        )
    )

    # place found fuel stations as markers on the map
    for node in result.nodes:

        print("")
        logging.info("Add tag at {lat}, {lon}".format(lat=node.lat, lon=node.lon))
        logging.info(node.tags)

        folium.map.Marker([node.lat, node.lon],
                          popup=node.tags.get('brand', TAG)).add_to(my_map)

logging.info("Saving map to file {output_file}".format(output_file=OUTPUT_FILE))

my_map.save(OUTPUT_FILE)

logging.info("Map saved - exiting the program")
