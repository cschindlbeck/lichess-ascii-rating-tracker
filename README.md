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

Last update: 27.09.2022 22:20:11
</code>
</pre>

Follow me on [![Lichess Badge](https://img.shields.io/static/v1?style=flat&message=Lichess&color=000000&logo=Lichess&logoColor=FFFFFF&label=)](https://lichess.org/@/christopsy666)

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
