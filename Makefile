BLACK_IGNORE=migrations
PYTHON=python

fmt:
	black --exclude "${BLACK_IGNORE}" .
	isort --recursive .

lint:
	flake8 .
	mypy .
	black --exclude "${BLACK_IGNORE}" --check .
	isort --recursive --check-only .

security:
	safety check
	bandit -r .

test:
	${PYTHON} manage.py collectstatic --no-input
	${PYTHON} manage.py compress --engine jinja2 --force
	${PYTHON} manage.py test --noinput -k
