"""LGA object"""

import time

import pygame


def reverse_tuple(tup):
    return tup[1], tup[0]


class LocalGovArea:
    """A pygame surface object that represents a local government area"""
    WINDOW_SIZE = (800, 800)

    def __init__(self, name, points_list, bounding):
        """Pass in name and points list

        bounding: tuple of tuples containing top left and bottom right of window area in grid coords
        """
        pygame.init()
        self.bounding = bounding
        self.points_list = points_list
        self.mapsurface = pygame.surface.Surface(self.WINDOW_SIZE, pygame.SRCALPHA, 32)
        self.trace_outline()
        self.mapsurface.set_colorkey((0, 0, 0))
        pygame.display.update()

    def dms_to_pix(self, coord, bounding):
        """Convert coordinates to pygame coordinate within the spatial boundary"""
        a = ((coord[0] - bounding[1][0]) / (bounding[1][0] - bounding[0][0])) * self.WINDOW_SIZE[0]
        b = ((coord[1] - bounding[0][1]) / (bounding[1][1] - bounding[0][1])) * self.WINDOW_SIZE[1]
        return int(abs(a)), int(abs(b))

    def trace_outline(self):
        pen = (255, 255, 255)
        outlinemapsurface = pygame.surface.Surface(self.WINDOW_SIZE)
        points = [self.dms_to_pix(reverse_tuple(point), self.bounding) for point in self.points_list]
        pygame.draw.polygon(outlinemapsurface, pen, points, width=2)
        newsurface = pygame.transform.rotate(outlinemapsurface, 90)
        self.mapsurface = pygame.transform.flip(newsurface, False, False)


def main():
    """"""
    # -33.391159, 150.501858 Up Left
    # -34.131313, 151.417080 Down Right
    map_window = ((-33.391159, 150.501858), (-34.131313, 151.417080))
    print("Starting")
    pygame.init()
    mapcanvas = pygame.display.set_mode((800, 800))
    a = LocalGovArea(None, geo_data["PARRAMATTA"], map_window)
    b = LocalGovArea(None, geo_data["INNER WEST"], map_window)
    c = LocalGovArea(None, geo_data["NORTHERN BEACHES"], map_window)
    d = LocalGovArea(None, geo_data["CANADA BAY"], map_window)
    mapcanvas.blit(a.mapsurface, (0, 0))
    mapcanvas.blit(b.mapsurface, (0, 0))
    mapcanvas.blit(c.mapsurface, (0, 0))
    mapcanvas.blit(d.mapsurface, (0, 0))
    pygame.display.update()
    time.sleep(8)


if __name__ == '__main__':
    from geodata import process_geodata, find_limits
    import sys
    import json
    with open(sys.argv[1]) as json_file:
        json_object = json.load(json_file)
    geo_data = process_geodata(json_object)
    unchanged_limits = find_limits(geo_data["PARRAMATTA"])
    limits = (reverse_tuple(unchanged_limits[0]), reverse_tuple(unchanged_limits[1]))
    # [print(x) for x in geo_data["PARRAMATTA"]]
    print(limits)
    main()
