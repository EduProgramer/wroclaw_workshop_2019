RADIUS = 2000
TAG = 'fuel'

# for more info about queries to overpass visit https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL
QUERY_TEMPLATE = '(node["amenity"="{tag}"](around:{radius},{lat},{lon}););out body;'

NTH_POINT = 500
OUTPUT_FILE = "map3.html"
