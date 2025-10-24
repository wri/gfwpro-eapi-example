import fiona

# define schema
schema = {
    "geometry": "Polygon",
    "properties": [
        ("Location_Name", "str"),
        ("Attr bC 1", "str"),
    ]
}

# open a fiona object
polyShp = fiona.open(
    "./sample-polygon-shapefile.shp",
    mode="w",
    driver="ESRI Shapefile",
    schema=schema,
    crs="EPSG:4326",
)

# define attribute table
attributeTable = {
    "Location_Name": "Loc1",
    "Attr bC 1": "A362",
}

# list of points in (long, lat) format
polyPoints = [
    (-65.9001, -27.0987),
    (-65.8001, -27.0987),
    (-65.8001, -27.1987),
    (-65.9001, -27.1987),
]

# save record and close shapefile
rowDict = {
    "type":"Feature",
    "properties": attributeTable,
    "geometry": {
        "type": "Polygon",
        "coordinates": [polyPoints],
    },
}
polyShp.write(rowDict)

# close fiona object
polyShp.close()

print("files generated")
