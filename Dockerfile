FROM python:3.8-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml /app/
COPY chatrapper/ /app/chatrapper/

RUN poetry install --only main

EXPOSE 9000

CMD ["uvicorn", "chatrapper.api:app", "--host", "0.0.0.0", "--port", "9000"]
