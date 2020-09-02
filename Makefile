PYTHON=python

fmt:
	black .
	isort --recursive .

lint:
	flake8 .
	mypy .
	black --check .
	isort --recursive --check-only .

security:
	safety check
	bandit -r .

test:
	${PYTHON} manage.py collectstatic --no-input
	${PYTHON} manage.py compress --engine jinja2 --force
	${PYTHON} manage.py migrate --no-input
	${PYTHON} manage.py test --noinput -k
