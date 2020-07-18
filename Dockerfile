FROM python:3.7.3-stretch

WORKDIR /app

# Setting up pipenv
RUN pip install --no-cache-dir -q pipenv
COPY Pipfile Pipfile.lock ./

ARG BUILD_PACKAGES="gcc g++ linux-headers-amd64 postgresql"
RUN apt-get update \
 && apt-get install -y locales libsass-dev libc-bin libjpeg-dev libxslt1-dev libpq-dev ${BUILD_PACKAGES} \
 && pipenv install --system --clear --dev

# Clear dependencies
RUN apt-get purge -y ${BUILD_PACKAGES} \
 && rm -rf /var/lib/apt/lists/* \
 && pip uninstall pipenv -y \
 && rm -r /root/.cache \
 && mkdir -p /static/media

# Setting up locales
RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
 && dpkg-reconfigure --frontend=noninteractive locales \
 && update-locale LANG=ru_RU.UTF-8

ENV LANG ru_RU.UTF-8

EXPOSE 8000

COPY . /app

CMD ["/app/entrypoint.sh"]
