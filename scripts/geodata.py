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
        else:
            # if a duplicate LGA name exists, add a number to the end.  {LGA_NAME}_{Count of dupes}
            existing_count = len([dup for dup in areas.keys() if dup.startswith(each["properties"]["nsw_lga__3"])])
            newkey = f"""{each["properties"]["nsw_lga__3"]}_{existing_count}"""
            areas[newkey] = each["geometry"]["coordinates"][0][0]
    return areas


def main(json_obj):
    """Convenience"""
    process_geodata(json_obj)


if __name__ == '__main__':
    with open(sys.argv[1]) as json_file:
        json_object = json.load(json_file)
    main(json_object)
