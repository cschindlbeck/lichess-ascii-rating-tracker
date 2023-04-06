init:
	pip install -r requirements.txt

test:
	python3 test/test_lichess_ascii_tracker.py

.PHONY: init test
