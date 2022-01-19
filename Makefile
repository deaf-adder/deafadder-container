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
	poetry run coverage report -m

generate-requirements:
	poetry export -f requirements.txt > requirements.txt

check-version:
	bash ./build-scripts/check_version.sh


lint:
	poetry run flake8


doc-serve:
	./node_modules/docsify-cli/bin/docsify serve docs


qodana:
	docker run --rm -it -v $$(pwd):/data/project/ -p 8080:8080 jetbrains/qodana-python --show-report