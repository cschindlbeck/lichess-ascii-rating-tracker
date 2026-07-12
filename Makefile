init:
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt

test:
	source venv/bin/activate && PYTHONPATH=. python3 test/test_lichess_ascii_tracker.py

.PHONY: init test
