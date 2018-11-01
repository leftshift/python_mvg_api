from mvg_api.mvg_api_requests import *

from colr import color
from texttable import Texttable

import sys
import os

MVG_BG = "#2a4779"
MVG_FG = "#ffffff"

class Departure:
    
    def __init__( self, obj ):
        self.json = obj

    def get_line(self):
        label = color(self.json["label"], fore="#fff", back=self.json["lineBackgroundColor"])
        return label

    def get_destination(self):
        return self.json["destination"]

    def get_departure_time_min(self):
        return self.json["departureTimeMinutes"]

    def get(self, *attributes ):
        row = []
        for attr in attributes:
            if attr == "label":
                row.append( self.get_line() )
            else:
                row.append( self.json[attr] )
        return row
    
    def __str__(self):
        label = self.get_line()
        direction = self.get_destination()
        departure_min = self.json["departureTimeMinutes"]

        return label + "\t" + direction + "\t" + str(departure_min)
        

def display_title_bar():
    # os.system('clear')
    bar = color("*" * 48, fore=MVG_FG, back=MVG_BG)
    fifteen_stars = "*" * 15
    print(bar)
    print(color(fifteen_stars + " MVG - Departures " + fifteen_stars, fore=MVG_FG, back=MVG_BG) )
    print(bar + "\n")

def display_departures(station_name, limit=20):
    departuresJSON = get_departures_by_name(station_name)
    departuresJSON = departuresJSON[:limit]

    departures = [ Departure(i) for i in departuresJSON ]
    
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype( ['t', 't', 'i'])
    table.set_cols_align( ['l', 'l', 'r'] )
    
    rows = []
    rows.append(['\x1b[38;5;231m\x1b[48;5;23mline\x1b[0m', 'destination', 'departure (min)'])
    for dep in departures:
        rows.append( dep.get("label", "destination", "departureTimeMinutes") )
    table.add_rows(rows)
    print( color(table.draw(), fore=MVG_FG, back=MVG_BG) )
    

path = os.path.dirname(os.path.abspath(__file__))

if len(sys.argv) == 2:
    display_departures(sys.argv[1])
    recent = open(path + "/recent.txt", "w")
    recent.write(sys.argv[1])
elif len(sys.argv) == 1:
    recent = open(path + "/recent.txt", "r")
    display_departures(recent.read())
else:
    display_departures("Studentenstadt")
