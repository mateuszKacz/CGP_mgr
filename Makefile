install:
	poetry install

notebook:
	poetry run jupyter notebook

lint:
	poetry run flakehell lint src

isort:
	poetry run isort src

black:
	poetry run black --config pyproject.toml src

format: isort black

check: format lint