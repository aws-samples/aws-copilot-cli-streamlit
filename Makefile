.DEFAULT_GOAL := help
.PHONY: coverage deps help lint publish push test tox

lint:
	black app/*.py
	flake8 app/*.py --ignore E501
	pylint --fail-under=7 app/*.py

#test:
# place holder for make test

install:
	python -m pip install --upgrade pip
	python -m pip install black flake8 pytest
	python -m pip install -r app/requirements.txt

install-dev: install
	python -m pip install -r requirements.dev
	pre-commit install

clean:
	rm -rf **/.ipynb_checkpoints **/.pytest_cache **/__pycache__ **/**/__pycache__ .ipynb_checkpoints .pytest_cache
