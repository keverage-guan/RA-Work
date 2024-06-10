import pandas as pd
import geopandas as gpd
from shapely import wkt

# reads tract data from raw data
def read_tracts(filepath):
    # if filename ends in csv
    if filepath.endswith('.csv'):
        tracts = pd.read_csv(filepath)
    if filepath.endswith('.shp') or filepath.endswith('.json'):
        tracts = gpd.read_file(filepath)

    # look for a column named the_geom, geometry, geom, polygon, or polygons
    for column in ['the_geom', 'geometry', 'geom', 'polygon', 'polygons']:
        if column in tracts.columns:
            geo_column = column
            break
    # look for column with TRACT in it
    for column in tracts.columns:
        if 'TRACT' in column:
            tract_column = column
            break
    
    tracts = tracts[[geo_column, tract_column]]
    tracts = tracts.rename(columns={geo_column: 'geometry', tract_column: 'TRACTCE'})
    if filepath.endswith('.csv'):
        tracts['geometry'] = tracts['geometry'].apply(wkt.loads)
    tracts = gpd.GeoDataFrame(tracts, geometry='geometry')

    return tracts

# determines tracts that overlap with a polygon
def overlap(tract_df, polygon):
    tracts = []
    percents = []
    for index, row in tract_df.iterrows():
        if row['geometry'].intersects(polygon):
            tracts.append(row['TRACTCE'])
            percents.append(row['geometry'].intersection(polygon).area / row['geometry'].area)

    return tracts, percents

# converts a list to a string
def list_to_string(lst):
    return '[' + ', '.join(map(str, lst)) + ']'
