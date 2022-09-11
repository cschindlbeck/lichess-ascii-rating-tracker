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
