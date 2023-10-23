from flask import Flask, request, jsonify
from flask_cors import CORS
import osmnx as ox
import geopandas as gpd

latitude = 19.20208333
longitude = 72.96747222
distance = 300  # Distance in meters (e.g., 1000 for a 1 km radius)


app = Flask(__name__)
CORS(app)

def building_maker(latitude, longitude, distance):
    G = ox.features.features_from_point((latitude, longitude), dist=distance, tags={"building": True})
    # G.plot()

    # G1 = ox.features.features_from_point((latitude, longitude), dist=distance, tags={"highway":True, "building":True})
    # G1.plot()

    # print(type(G))

    coordinates_list = []

    # Iterate through each geometry (polygon) in the GeoDataFrame
    for geom in G['geometry']:
        # Extract the x and y coordinates of the polygon and convert them to a list of tuples
        coordinates = [(x, y) for x, y in zip(geom.exterior.coords.xy[0], geom.exterior.coords.xy[1])]
        coordinates_list.append(coordinates)

    # Now, coordinates_list contains a list of polygons with their coordinates
    # print(coordinates_list[0])

    x_centers = []
    y_centers = []

    for i in coordinates_list:
        x_sum = 0
        y_sum = 0
        i = i[:-1]
        # print(len(i))
        for j in i:
            x_sum = x_sum + j[0]
            y_sum = y_sum + j[1]
        x_avg = x_sum / (len(i))
        y_avg = y_sum / (len(i))
        x_centers.append(x_avg)
        y_centers.append(y_avg)

    # print(len(coordinates_list[0]))

    x_cent_sum = 0
    y_cent_sum = 0
    for i in x_centers:
        x_cent_sum = x_cent_sum + i
    for i in y_centers:
        y_cent_sum = y_cent_sum + i

    x_cent_sum = x_cent_sum / len(x_centers)
    y_cent_sum = y_cent_sum / len(y_centers)

    norm_coordinates_list = []

    for i in coordinates_list:
        neww = []
        i = i[:-1]
        for j in i:
            x_new = (j[0] - x_cent_sum)*800
            y_new = (j[1] - y_cent_sum)*800
            tupp = (x_new, y_new)
            neww.append(tupp)
        norm_coordinates_list.append(neww)

    print(norm_coordinates_list[0])
    print(norm_coordinates_list[1])
    print(len(norm_coordinates_list[0]))

    norm_x_cents=[]
    norm_y_cents=[]

    for k in x_centers:
        new_x_cent=(k-x_cent_sum)*10
        norm_x_cents.append(new_x_cent)

    for k in y_centers:
        new_y_cent=(k-y_cent_sum)*10
        norm_y_cents.append(new_y_cent)

    # probably need to itterate thru the coordinates and scale them to a certain size but for now cool nuff

    return (norm_coordinates_list, norm_x_cents, norm_y_cents )


@app.route('/call_python_function', methods=['POST'])
def call_python_function():
    # Call your Python function here
    norm, xcent, ycent = building_maker(latitude=latitude, longitude=longitude, distance=distance)
    return jsonify({'norm': norm, 'xcent': xcent, 'ycent':ycent })

if __name__ == '__main__':
    app.run()
