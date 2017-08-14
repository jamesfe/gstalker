.PHONY: test
test:
	python3 -m unittest discover -v

.PHONY: run
run:
	python3 ./gstalker/main.py
