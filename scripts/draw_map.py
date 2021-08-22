"""Build a map"""
import json
import sys
import time

import numpy as np
import pandas as pd
import pygame

import geodata
import covid_stats
from LGA import LocalGovArea


def main():
    exclusions = ["BLUE MOUNTAINS",
                  "WOLLONDILLY",
                  "WOLLONGONG_2"
                  ]
    map_window = ((-33.391159, 150.501858), (-34.131313, 151.417080))
    pygame.init()
    mapcanvas = pygame.display.set_mode((800, 800))
    with open('../geodata/lga_boundary.json') as json_file:
        json_object = json.load(json_file)
    gd = geodata.process_geodata(json_object)
    viewable_lgas = dict()
    lga_objects = dict()
    for k, v in gd.items():
        if geodata.inbounds(v, map_window):
            viewable_lgas[k] = v
    for lga, point_data in viewable_lgas.items():
        if lga in exclusions:
            continue
        lga_objects[lga] = LocalGovArea(None, viewable_lgas[lga], map_window)
        mapcanvas.blit(lga_objects[lga].mapsurface, (0, 0))
        pygame.display.update()

    for idx, row in covid_stats.get_covid_data('../covid_data/confirmed_cases_table1_location.csv').iterrows():
        for lga_name, value in row.items():
            if not np.isnan(value):
                # print(covid_stats.clean_lga(lga_name), value)
                try:
                    red = int(value) * 7
                    if red > 255:
                        red = 255
                    lga_objects[covid_stats.clean_lga(lga_name)].trace_outline((red, 0, 0), fill=True)
                    mapcanvas.blit(lga_objects[covid_stats.clean_lga(lga_name)].mapsurface, (0, 0))
                    lga_objects[covid_stats.clean_lga(lga_name)].trace_outline((255, 255, 255))
                    mapcanvas.blit(lga_objects[covid_stats.clean_lga(lga_name)].mapsurface, (0, 0))
                except KeyError:
                    pass
                    # print(f"{lga_name} is not found")
        pygame.display.update()
    time.sleep(2)
    pygame.display.update()
    time.sleep(12)


if __name__ == '__main__':
    main()
