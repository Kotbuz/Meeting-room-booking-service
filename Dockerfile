FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml ./

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root && poetry cache clear pypi --all 
COPY . . 
CMD ["python", "app/main.py"]