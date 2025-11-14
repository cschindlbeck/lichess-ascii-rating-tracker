init:
	pip install -r requirements.txt

test:
	PYTHONPATH=. python3 test/test_lichess_ascii_tracker.py

.PHONY: init test
