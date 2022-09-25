

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
