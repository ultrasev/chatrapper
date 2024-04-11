FROM python:3.8-slim

WORKDIR /app

RUN pip install poetry

COPY . /app

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 9000

CMD ["uvicorn", "chatrapper.api:app", "--host", "0.0.0.0", "--port", "9000"]
