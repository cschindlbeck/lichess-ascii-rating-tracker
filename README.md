<!-- [![Coverage Status](https://coveralls.io/repos/github/kroitor/asciichart/badge.svg?branch=master)](https://coveralls.io/github/kroitor/asciichart?branch=master) -->
[![license](https://img.shields.io/github/license/kroitor/asciichart.svg)](https://github.com/kroitor/asciichart/blob/master/LICENSE.txt)
![pylint workflow](https://github.com/cschindlbeck/lichess-ascii-rating-tracker/actions/workflows/pylint.yml/badge.svg)
![pylint workflow](https://github.com/cschindlbeck/lichess-ascii-rating-tracker/actions/workflows/docker-image.yml/badge.svg)
# Lichess ASCII rating tracker

Generates lichess ASCII rating tracker.

Follow me on [![Lichess Badge](https://img.shields.io/static/v1?style=flat&message=Lichess&color=000000&logo=Lichess&logoColor=FFFFFF&label=)](https://lichess.org/@/christopsy666)

## Installation

Install the python dependencies via requirements.txt

```bash
export API_TOKEN=your_lichess_api_token
```

```bash
export PUZZLE_TYPE=Bullet
```

## Usage

```bash
python3 lichess_ascii_rating_tracker.py
```


## Docker

```bash
cd .docker

docker compose build lichess

docker compose run lichess
```

Output can be piped to a file

## Examples

christopsy666
Puzzles
    1978 ┤  
    1935 ┤        ╭╮                  ╭╮  ╭─╮  
    1892 ┤        │╰─╮╭──╮  ╭╮  ╭╮╭╮ ╭╯│ ╭╯ ╰╮
    1849 ┤        │  ╰╯  ╰╮╭╯│╭─╯╰╯╰─╯ ╰─╯   │ ╭─╮    ╭
    1806 ┤        │       ╰╯ ╰╯              │ │ ╰──╮ │
    1762 ┤        │                          ╰─╯    ╰─╯
    1719 ┤        │
    1676 ┼╮╭╮ ╭╮  │
    1633 ┤╰╯│ │╰─╮│
    1590 ┤  │ │  ╰╯
    1547 ┤  ╰─╯
christopsy666
Puzzles
'    1978 ┤\n    1935 ┤        ╭╮                  ╭╮  ╭─╮\n    1892 ┤        │╰─╮╭──╮  ╭╮  ╭╮╭╮ ╭╯│ ╭╯ ╰╮\n    1849 ┤        │  ╰╯  ╰╮╭╯│╭─╯╰╯╰─╯ ╰─╯   │ ╭─╮    ╭\n    1806 ┤        │       ╰╯ ╰╯              │ │ ╰──╮ │\n    1762 ┤        │                          ╰─╯    ╰─╯\n    1719 ┤        │\n    1676 ┼╮╭╮ ╭╮  │\n    1633 ┤╰╯│ │╰─╮│\n    1590 ┤  │ │  ╰╯\n    1547 ┤  ╰─╯'
