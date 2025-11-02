pn = 'sample-langflow-mcp'

init: ## 開発作成
	docker compose -p $(pn) build --no-cache
	docker compose -p $(pn) down --volumes
	docker compose -p $(pn) up -d
	docker compose -p $(pn) exec -it mcp pipenv install --dev
	make opensearch-setup

opensearch-setup:
	docker compose -p $(pn) exec -it mcp pipenv run python scripts/opensearch_setup.py

up: ## 開発立ち上げ
	docker compose -p $(pn) up -d

down: ## 開発down
	docker compose -p $(pn) down

restart: ## 開発再起動
	make down
	make up

mcp-shell: ## dockerのshellに入る
	docker compose -p $(pn) exec mcp bash

opensearch-script-shell: ## dockerのshellに入る
	docker compose -p $(pn) exec opensearch-script bash


langflow-shell: ## dockerのshellに入る
	docker compose -p $(pn) exec langflow bash

check: ## コードのフォーマット
	docker compose -p $(pn) exec -it mcp pipenv run isort .
	docker compose -p $(pn) exec -it mcp pipenv run black .
	docker compose -p $(pn) exec -it mcp pipenv run flake8 .
	docker compose -p $(pn) exec -it mcp pipenv run mypy .

destroy: ## 環境削除
	make down
	docker network ls -qf name=$(pn) | xargs docker network rm
	docker container ls -a -qf name=$(pn) | xargs docker container rm
	docker volume ls -qf name=$(pn) | xargs docker volume rm

push:
	git add .
	git commit -m "Commit at $$(date +'%Y-%m-%d %H:%M:%S')"
	git push origin head

mcp-run:
# 	docker compose -p $(pn) exec -it mcp pipenv run fastmcp run main.py:mcp --transport http --port 8000
	docker compose -p $(pn) exec -it mcp pipenv run fastmcp run main.py:mcp
