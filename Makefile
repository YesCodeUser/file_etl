IMAGE_NAME=file_etl-app

FILE=
NO_DB=
JSON=

build:
	docker build -t $(IMAGE_NAME) .

up:
	docker compose up -d postgres

run:
	docker compose run --rm app $(FILE) $(NO_DB) $(JSON)

down:
	docker compose down

logs:
	docker compose logs -f