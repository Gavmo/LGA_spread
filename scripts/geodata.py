import copy
import json
import sys


# -33.391159, 150.501858 Up Left
# -34.131313, 151.417080 Down Right


def process_geodata(json_obj):
    """Extract LGA boundary data

    Return a dictionary with LGA name and boundary data.
    {
        "BURWOOD": [[lat, lon], [lat, lon], ..., ...],
        "PARRAMATTA": [[lat, lon], [lat, lon], ..., ...],
        ...
    }
    """
    areas = {}
    for each in json_obj["features"]:
        if each["properties"]["nsw_lga__3"] not in areas and not each["properties"]["nsw_lga__3"].startswith("UNINCOR"):
            areas[each["properties"]["nsw_lga__3"]] = each["geometry"]["coordinates"][0][0]
        elif not each["properties"]["nsw_lga__3"].startswith("UNINCOR"):
            # if a duplicate LGA name exists, add a number to the end.  {LGA_NAME}_{Count of dupes}
            existing_count = len([dup for dup in areas.keys() if dup.startswith(each["properties"]["nsw_lga__3"])])
            newkey = f"""{each["properties"]["nsw_lga__3"]}_{existing_count}"""
            areas[newkey] = each["geometry"]["coordinates"][0][0]
    return areas


def find_limits(point_list):
    """Find the upper and lower limits of a lis of points"""
    upper = copy.copy(point_list[0])
    lower = copy.copy(point_list[0])
    for point in point_list[1:]:
        if point[0] > upper[0]:
            upper[0] = copy.copy(point[0])
        if point[0] < lower[0]:
            lower[0] = copy.copy(point[0])
        if point[1] > upper[1]:
            upper[1] = copy.copy(point[1])
        if point[1] < lower[1]:
            lower[1] = copy.copy(point[1])
    return upper, lower


def inbounds(point_list, bounds):
    """Check to see if at least one point is within the viewing window"""
    for point in point_list:
        if bounds[0][1] <= point[0] <= bounds[1][1]:
            if bounds[1][0] <= point[1] <= bounds[0][0]:
                return True


def main(json_obj):
    """Convenience"""
    a = process_geodata(json_obj)
    map_window = ((-33.391159, 150.501858), (-34.131313, 151.417080))
    for k, v in a.items():
        if inbounds(v, map_window):
            print(k)


if __name__ == '__main__':
    with open(sys.argv[1]) as json_file:
        json_object = json.load(json_file)
    main(json_object)

