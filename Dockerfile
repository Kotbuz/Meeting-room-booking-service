FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PIP_NO_CACHE_DIR=1
ENV PATH="/root/.local/bin:$PATH"

RUN pip install --upgrade pip "poetry>=2.0,<3.0"

COPY pyproject.toml README.md ./

RUN poetry config virtualenvs.create false \
    && poetry lock \
    && poetry install --only main --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]