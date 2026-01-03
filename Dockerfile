FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install --no-cache-dir .

COPY . .

ENTRYPOINT ["python3", "-m", "app"]
CMD ["--help"]