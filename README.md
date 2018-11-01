# A console program to request the departure time from the MVG

The python program is based on the library by [leftshift](https://github.com/leftshift/python_mvg_api). Check out his work for more info on the API.

## Getting started

`git clone https://github.com/frankzl/python_mvg_console_program`

Then add the following line to your `.zshrc`

`alias mvg="python3.5 $HOME/path/to/directory/python_mvg_console_program/get_info.py"`

Probably not the cleanest way to do it, but it's the only way I know at the moment :)

Please feel free to correct me anywhere if you have a better idea!

## Run
`mvg Studentenstadt` will look up all the departures from the station "Studentenstadt"

`mvg` will run the last station you have looked up

## Demo
![screenshot](demo.png)
