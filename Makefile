PYTHON=python
CI_REGISTRY_IMAGE=ghcr.io/assisken/zhipa
USER=$(shell id -u)
GROUP=$(shell id -g)
DOCKER_TEST=docker run -v "${PWD}:/app" --rm -it -e ENV="testing" "${CI_REGISTRY_IMAGE}":latest

docker-pull:
	docker pull "${CI_REGISTRY_IMAGE}"

docker-build: docker-pull
	docker build --cache-from "${CI_REGISTRY_IMAGE}":latest --tag "${CI_REGISTRY_IMAGE}":latest .

docker-test:
	${DOCKER_TEST} ./manage.py collectstatic --no-input
	${DOCKER_TEST} ./manage.py compress --engine jinja2 --force
	${DOCKER_TEST} ./manage.py migrate --no-input
	${DOCKER_TEST} ./manage.py test --noinput

fmt:
	black .
	isort .

lint:
	flake8 .
	mypy .
	black --check .
	isort --check-only .

test:
	${PYTHON} ./manage.py collectstatic --no-input
	${PYTHON} ./manage.py compress --engine jinja2 --force
	${PYTHON} ./manage.py migrate --no-input
	${PYTHON} ./manage.py test --noinput

update-initial-data:
	docker exec -it smiap-app ./manage.py dumpdata --format=json --indent=4 -o init/initial.json
