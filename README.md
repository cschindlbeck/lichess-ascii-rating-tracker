<!-- [![Coverage Status](https://coveralls.io/repos/github/kroitor/asciichart/badge.svg?branch=master)](https://coveralls.io/github/kroitor/asciichart?branch=master) -->
[![license](https://img.shields.io/github/license/kroitor/asciichart.svg)](https://github.com/kroitor/asciichart/blob/master/LICENSE.txt)
![pylint workflow](https://github.com/cschindlbeck/lichess-ascii-rating-tracker/actions/workflows/pylint.yml/badge.svg)
![docker workflow](https://github.com/cschindlbeck/lichess-ascii-rating-tracker/actions/workflows/docker-image.yml/badge.svg)
![build readme](https://github.com/cschindlbeck/lichess-ascii-rating-tracker/actions/workflows/build-readme.yml/badge.svg)

# &#9816; Lichess ASCII rating generator

Generates ASCII charts of [lichess](https://lichess.org/) ratings.

Example:

<pre>
<code>

          _      _      _
         | |    (_)    | |
         | |     _  ___| |__   ___  ___ ___
         | |    | |/ __| '_ \ / _ \/ __/ __|
         | |____| | (__| | | |  __/\__ \__ \
         |______|_|\___|_| |_|\___||___/___/
        
    1934 ┤
    1866 ┤                                              ╭──╮╭──╮    ╭─╮
    1797 ┤                                ╭╮     ╭╮╭╮ ╭─╯  ╰╯  ╰╮╭──╯ ╰─
    1729 ┤                           ╭╮  ╭╯╰╮╭──╮│╰╯╰─╯         ╰╯
    1660 ┤                          ╭╯│╭╮│  ╰╯  ╰╯
    1592 ┤                      ╭╮╭╮│ ╰╯╰╯
    1524 ┼╮    ╭──╮      ╭╮╭────╯╰╯╰╯
    1455 ┤│   ╭╯  │╭─╮╭╮╭╯╰╯
    1387 ┤╰╮ ╭╯   ╰╯ ╰╯╰╯
    1318 ┤ │╭╯
    1250 ┤ ╰╯

User: christopsy666, Rating type: Bullet on lichess.org
Last update: 06.04.2023 20:28:37
</code>
</pre>

Follow me on [![Lichess Badge](https://img.shields.io/static/v1?style=flat&message=Lichess&color=000000&logo=Lichess&logoColor=FFFFFF&label=)](https://lichess.org/@/christopsy666)

## Installation

Install the python dependencies via requirements.txt via

```bash
pip install -r requirements.txt
```

and export your lichess API token as environment variables via

```bash
export API_TOKEN=your_lichess_api_token
```

For convenience, put this in you .bashrc

## Usage

```bash
python3 lichess_ascii_rating_tracker.py -r puzzle_type
```

where puzzle_type is one of the following:

Bullet, Blitz, Rapid, Classical, Correspondence, Chess960, King of the Hill, Three-check, Antichess, Atomic, Horde, Racing Kings, Crazyhouse, Puzzles, UltraBullet

The output can be piped to a file, but should be enclosed with

```html
<pre>
<code>
generated_output
</code>
</pre>
```

for Markdown to preserve whitespaces.

## Docker

Alternatively, you can use docker compose to generate an ASCII chart.

First, build the image via

```bash
cd .docker
docker compose build
```

and then run it via

```bash
docker run -it -e API_TOKEN=$API_TOKEN lichess-docker:v0.1.0 -r Bullet
```
