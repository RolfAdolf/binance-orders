FROM python:3.10.6

RUN mkdir /app

WORKDIR /app

RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false

RUN poetry install

RUN chmod a+x docker/*.sh

# CMD ["bash", "docker/run_main_with_tests.sh"]