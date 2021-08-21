import geopandas
import json

shp_path = '/home/budi/indonesian_government/indonesian_province_geospatial/prov.shp'
geojson_path = '/home/budi/indonesian_government/indonesian_province_geospatial/prov.geojson'

shp_file = geopandas.read_file(shp_path)
shp_file.to_file(geojson_path, driver='GeoJSON')