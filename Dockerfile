FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry \
 && poetry config virtualenvs.in-project true --local \
 && poetry install --no-root --only main

ENV PATH="/code/.venv/bin:$PATH"

COPY . .

WORKDIR /code/src/website

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn website.wsgi:application --bind 0.0.0.0:8000"]
