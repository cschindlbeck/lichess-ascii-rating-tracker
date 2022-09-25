<!-- [![Coverage Status](https://coveralls.io/repos/github/kroitor/asciichart/badge.svg?branch=master)](https://coveralls.io/github/kroitor/asciichart?branch=master) -->
[![license](https://img.shields.io/github/license/kroitor/asciichart.svg)](https://github.com/kroitor/asciichart/blob/master/LICENSE.txt)
![pylint workflow](https://github.com/cschindlbeck/lichess-ascii-rating-tracker/actions/workflows/pylint.yml/badge.svg)
![docker workflow](https://github.com/cschindlbeck/lichess-ascii-rating-tracker/actions/workflows/docker-image.yml/badge.svg)
![build readme](https://github.com/cschindlbeck/lichess-ascii-rating-tracker/actions/workflows/build-readme.yml/badge.svg)

# Lichess ASCII chart generator

Generates ASCII charts of Lichess ratings. Seamless CI integration for updating it.

Example:

<pre>
<code>
User: christopsy666, Rating type: Blitz on lichess.org

    1776 ┤                                                                      ╭
    1736 ┤                                                                      │
    1696 ┤                                                                 ╭────╯
    1656 ┤                                     ╭╮                    ╭─────╯
    1616 ┤                                 ╭───╯╰────────────╮╭╮  ╭──╯
    1576 ┤                      ╭╮ ╭╮     ╭╯                 ╰╯╰──╯
    1535 ┤ ╭╮    ╭─╮╭────╮╭╮╭───╯╰╮│╰─────╯
    1495 ┤ │╰╮╭──╯ ╰╯    ╰╯╰╯     ╰╯
    1455 ┤╭╯ ╰╯
    1415 ┼╯
    1375 ┤

Last update: 25.09.2022 12:48:34
</code>
</pre>
  
## Installation

Install the python dependencies via requirements.txt via

```bash
pip install -r requirements.txt
```

and export the environment variables via

```bash
export API_TOKEN=your_lichess_api_token
export PUZZLE_TYPE=Bullet
```

For convenience, put them in you .bashrc

## Usage

```bash
python3 lichess_ascii_rating_tracker.py
```

The output can be piped to a file

## Docker

Alternatively, you can use docker compose to generate an ascii chart.

First, build the image via

```bash
cd .docker
docker compose build lichess
```

and then run it via

```bash
docker compose run lichess
```
