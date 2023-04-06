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
