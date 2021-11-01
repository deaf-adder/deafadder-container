.ONEHSELL:
SHELL = /bin/bash
test:
	source .venv/bin/activate
	poetry run pytest


.ONEHSELL:
SHELL = /bin/bash
coverage:
	source .venv/bin/activate
	poetry run coverage run -m pytest
	poetry run coverage report


check-version:
	bash ./build-scripts/check_version.sh


lint:
	poetry run flake8


