import Vertix
import csv
import math
import subprocess
import os
import openpyxl
import copy
import threading
import random
import folium


class Tools:
    """This is a tools class"""

    @staticmethod
    def soltuionPathWriter(fileName, solutionsList, terminalsList):
        with open(fileName, 'w') as file:
            for terminal in terminalsList:
                file.write('%s \n \n' %(solutionsList[terminal].pathFinder(solutionsList, terminal)))

    @staticmethod
    def distanceCalculationMethod(vertix1 = Vertix, vertix2 = Vertix):
        """returns the distance between the two vertices according to Haversine Distance calculation method"""
        lat1 = vertix1.getx()
        lon1 = vertix1.gety()
        lat2 = vertix2.getx()
        lon2 = vertix2.gety()
        radius = 6371 # km

        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c

        return d

    @staticmethod
    def sectorFilesCleaner(directory):
        files = os.listdir(directory)
        for file in files:
            if file.endswith(".xlsx") or file.endswith(".dat"):
                os.remove(os.path.join(directory,file))
        print ('Files Cleaned!')
        return 0