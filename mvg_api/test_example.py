from __init__ import *

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
    print(color("****************************", fore=MVG_FG, back=MVG_BG))
    print(color("***** MVG - Departures *****", fore=MVG_FG, back=MVG_BG) )
    print(color("****************************", fore=MVG_FG, back=MVG_BG) + "\n")

def display_departures(station_name):
    departuresJSON = get_departures_by_name(station_name)

    departures = [ Departure(i) for i in departuresJSON ]
    
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype( ['t', 't', 'i'])
    table.set_cols_align( ['c', 'l', 'c'] )
    
    rows = []
    rows.append(['\x1b[38;5;231m\x1b[48;5;23mline\x1b[0m', 'destination', 'departureTime (min)'])
    for dep in departures:
        rows.append( dep.get("label", "destination", "departureTimeMinutes") )
    table.add_rows(rows)
    print( table.draw() )


if len(sys.argv) == 1:
    print(sys.argv)

display_title_bar()
display_departures("Studentenstadt")