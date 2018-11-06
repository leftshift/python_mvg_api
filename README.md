# A console program to request the departure time from the MVG

This python script is based on the MVG API by [leftshift](https://github.com/leftshift/python_mvg_api). Check out his work for more info on the API.

## Getting started

`git clone https://github.com/frankzl/python_mvg_console_program`

If you don't have pipenv, install it with pip:
`pip install pipenv`

Open a `pipenv shell` to install the dependencies:
```
$ pipenv shell
(mvg-program) $ pipenv install
```

Then add an alias to your shell, for example for ZSH add the following line to your `.zshrc`:

`alias mvg="python3 $HOME/path/to/directory/python_mvg_console_program/get_info.py"`

## Usage
<code>
  usage: mvg [-h] [--recent] [--departures DEPARTURES] [--limit LIMIT]

  arguments:
  -h, --help            show this help message and exit
  --recent, -r          fetch the most recent search.
  --departures DEPARTURES, -d DEPARTURES Departure Station/Stop
  --limit LIMIT, -l LIMIT # results to fetch

</code>

## Demo
![screenshot](demo.png)
