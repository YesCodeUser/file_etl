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

tg_bot-up:
	docker compose up -d telegram_bot

tg_bot-logs:
	docker compose logs -f telegram_bot

tg_bot-stop:
	docker compose stop telegram_bot

tg_bot-restart:
	docker compose restart telegram_bot

tg_bot-down:
	docker compose down telegram_bot
