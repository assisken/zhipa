FROM python:3.7.3-stretch

WORKDIR /app

# Setting up pipenv
COPY Pipfile Pipfile.lock ./

# Install packages, build, clear dependencies and setup lang
ARG BUILD_PACKAGES="gcc g++ linux-headers-amd64 postgresql"
RUN pip install --no-cache-dir -q pipenv \
 && apt-get update \
 && apt-get install -y locales libsass-dev libc-bin libjpeg-dev libxslt1-dev libpq-dev ${BUILD_PACKAGES} \
 && pipenv install --system --clear --dev \
 && apt-get purge -y ${BUILD_PACKAGES} \
 && rm -rf /var/lib/apt/lists/* \
 && pip uninstall pipenv -y \
 && rm -r /root/.cache \
 && mkdir -p /static/media \
 && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
 && dpkg-reconfigure --frontend=noninteractive locales \
 && update-locale LANG=ru_RU.UTF-8

ENV LANG ru_RU.UTF-8
EXPOSE 8123
COPY . /app

CMD ["/app/entrypoint.sh"]
