# coding=utf-8

from mvg_api.mvg_api_requests import *

from colr import color
from texttable import Texttable

import sys
import os

from pprint import  pprint

MVG_BG = "#2a4779"
MVG_FG = "#ffffff"

######
# Types of Transports
# 1. UBAHN
# 2. BUS
# 3. REGIONAL_BUS
# 4. TRAM
# 5. SBAHN
#######


class Departure:
    
    def __init__( self, json ):
        self.label = json["label"]
        self.destination = json["destination"]
        self.departure_time_minutes = json["departureTimeMinutes"]
        self.line_background_color = json["lineBackgroundColor"]
        self.product = json["product"]


    def get_label_colored(self):
        return color(self.label, fore="#fff", back=self.line_background_color)
    
    def __str__(self):
        label = self.get_label_colored()
        direction = self.destination
        departure_min = self.departure_time_minutes

        return label + "\t" + direction + "\t" + str(departure_min)
        

def display_title_bar():
    """ Print a title bar. """

    color_it_mvg = lambda x: color(x, fore=MVG_FG, back=MVG_BG)
    bar_mvg_colored = color_it_mvg("*" * 48)
    fifteen_stars = "*" * 15

    print(bar_mvg_colored)
    print(color_it_mvg(fifteen_stars + " MVG - Departures " + fifteen_stars))
    print(bar_mvg_colored + "\n")


def display_departures(station_name, limit=10, mode=None):
    station_name = get_station_name(station_name)
    departuresJSON = get_departures_by_name(station_name)
    departures = [ Departure(i) for i in departuresJSON ]
    #if mode is not None:
    departures = departures[:limit]
    
    print('\nStation: '+station_name+'\n')
    
    
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype( ['t', 't', 'i'])
    table.set_cols_align( ['l', 'l', 'r'] )
    
    rows = []
    rows.append(['\x1b[38;5;231m\x1b[48;5;23mline\x1b[0m', 'destination', 'departure (min)'])
    for dep in departures:
        rows.append( [dep.get_label_colored(), dep.destination, dep.departure_time_minutes] )
    table.add_rows(rows)
    print( color(table.draw(), fore=MVG_FG, back=MVG_BG) )
    


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(prog="mvg")
    #args_group = parser.add_mutually_exclusive_group()
    args_group = parser
    args_group.add_argument("--recent", "-r", action="store_true", help="fetch the most recent search.")
    args_group.add_argument("--departures", "-d", help="Departures at Station/Stop")
    args_group.add_argument("--limit", "-l", help="# results to fetch")
    args_group.add_argument("--mode", "-m", help="[List]Transportation Mode: bus, ubahn, sbahn, tram.", nargs='+')
    args = parser.parse_args()

    recents_file_path = os.path.join(os.getcwd(), "recent.txt")

    if args.recent:
        with open(recents_file_path, "r") as recent:
            display_departures(recent.read())
    elif args.departures: 
        #print(args.limit)
        if args.limit:
            display_departures(args.departures, int(args.limit), args.mode)
        else:
            display_departures(args.departures, mode=args.mode)
        with open(recents_file_path, "w") as recent:
            recent.write(args.departures)
    else:
        with open(recents_file_path, "r") as recent:
            display_departures(recent.read())

