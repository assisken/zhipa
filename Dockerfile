FROM python:3.7.3-stretch

# Setting up locales
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y locales

RUN sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
 && dpkg-reconfigure --frontend=noninteractive locales \
 && update-locale LANG=ru_RU.UTF-8

ENV LANG ru_RU.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Setting up packages
COPY requirements.txt /app/requirements.txt
RUN pip install --trusted-host pypi.python.org -r /app/requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 8000

# Run application when container launches
RUN python manage.py collectstatic
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]