PYTHON=python
CI_REGISTRY_IMAGE=registry.gitlab.com/assisken/zhipa
USER=$(shell id -u)
GROUP=$(shell id -g)

docker-pull:
	docker pull "${CI_REGISTRY_IMAGE}"

docker-build: pull
	docker build --cache-from "${CI_REGISTRY_IMAGE}":latest --tag "${CI_REGISTRY_IMAGE}":latest .

docker-fmt:
	docker run -v "${PWD}:/app" -u "${USER}:${GROUP}" --rm -it "${CI_REGISTRY_IMAGE}":latest black .
	docker run -v "${PWD}:/app" -u "${USER}:${GROUP}" --rm -it "${CI_REGISTRY_IMAGE}":latest isort --recursive .

docker-lint:
	docker run -v "${PWD}:/app" -u "${USER}:${GROUP}" --rm -it "${CI_REGISTRY_IMAGE}":latest flake8 .
	docker run -v "${PWD}:/app" -u "${USER}:${GROUP}" --rm -it "${CI_REGISTRY_IMAGE}":latest mypy .
	docker run -v "${PWD}:/app" -u "${USER}:${GROUP}" --rm -it "${CI_REGISTRY_IMAGE}":latest black --check .
	docker run -v "${PWD}:/app" -u "${USER}:${GROUP}" --rm -it "${CI_REGISTRY_IMAGE}":latest isort --recursive --check-only .

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
