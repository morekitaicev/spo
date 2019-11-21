import pandas as pd
import geopandas as gpd
import json
import folium

def json_to_geojson(data, districts):
    assert type(data) == list

    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "name": district,
                    "coordinates": [[[d["lon"], d["lat"]] for d in data if d['name'] == district]],
                },
                "properties": {'name': district},

            } for district in districts]
    }

    return geojson

with open('district_coords.txt', 'r') as fp:
    district_coords = json.loads(fp.read())

# get a list of districts
districts = list(set([district_coord['name'] for district_coord in district_coords]))

# create a geojson
geojson = json_to_geojson(district_coords, districts)

gdf = gpd.GeoDataFrame.from_features(geojson)
gdf['centroid_lon'] = gdf['geometry'].centroid.x
gdf['centroid_lat'] = gdf['geometry'].centroid.y
gdf.crs = {'init' :'epsg:4326'}


yavka = pd.read_csv('election_data.csv', sep=';')
yavka.columns = ['TIK', 'percent']
gdf_yavka = gdf.merge(yavka, left_on='name', right_on='TIK')

yavka_beglov = pd.read_csv('beglov_data.csv', sep=';')
yavka_beglov.columns = ['TIK', 'beglov']
gdf_beglov = gdf.merge(yavka_beglov, left_on='name', right_on='TIK')

m = folium.Map(location=[59.9375, 30.3066], zoom_start=11)

## add chloropleth layer
m.choropleth(
    geo_data=geojson,
    name='Yavka percent',
    data=gdf_yavka,
    columns=['name', 'percent'],
    fill_color='BuGn',
    key_on='feature.geometry.name',
    legend_name='Yavka percent'
)

fg = folium.FeatureGroup(name='TIK Info')
for lat, lon, val, name in zip(gdf_yavka['centroid_lat'].tolist(), gdf_yavka['centroid_lon'].tolist(), gdf_yavka['percent'].tolist(), gdf_yavka['name'].tolist()):
    html = f"""
    <h2>Saint Petersburg's {name}<\h2><br>
    <h4>Yavka: {float(round(val,4))} % <\h4>
    """
    fg.add_child(folium.Marker(location=[lat, lon], popup=html))

m.add_child(fg)

# enable layers to be turned in or out
folium.LayerControl().add_to(m)

# save it
m.save('yavka_percent.html')



t = folium.Map(location=[59.9375, 30.3066], zoom_start=11)

## add chloropleth layer
t.choropleth(
    geo_data=geojson,
    name='Yavka percent',
    data=gdf_beglov,
    columns=['name', 'beglov'],
    fill_color='OrRd',
    key_on='feature.geometry.name',
    legend_name='Beglov percent'
)

tg = folium.FeatureGroup(name='Beglov Info')
for lat, lon, val, name in zip(gdf_beglov['centroid_lat'].tolist(), gdf_beglov['centroid_lon'].tolist(), gdf_beglov['beglov'].tolist(), gdf_beglov['name'].tolist()):
    html = f"""
    <h2>Saint Petersburg's {name}<\h2><br>
    <h4>Beglov yavka: {float(round(val,4))} % <\h4>
    """
    tg.add_child(folium.Marker(location=[lat, lon], popup=html))

t.add_child(tg)

# enable layers to be turned in or out
folium.LayerControl().add_to(t)

# save it
t.save('beglov_percent.html')
