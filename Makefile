install:
	poetry install

test:
	poetry run pytest -vv

lint:
	poetry run flake8 page_loader

build:
	rm -rf dist
	poetry build

package-install:
	python3 -m pip install dist/*.whl --force-reinstall