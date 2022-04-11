rmi:
	@docker rmi todo_example_app

up:
	@docker-compose -f local.yml up -d --remove-orphans


build:
	@docker-compose -f local.yml build

down:
	@docker-compose -f local.yml down

run:
	@make -s build
	@make -s up
	@docker images -q -f dangling=true | xargs docker rmi -f

restart:
	@make -s down
	@make -s up

cmm:
	@make -s collectstatic
	@make -s makemigrations
	@make -s migrate

shell:
	@docker-compose -f local.yml exec app python manage.py shell

ps:
	@docker-compose -f local.yml ps

bash:
	@docker-compose -f local.yml exec app bash

test:
	docker-compose -f local.yml exec app ./manage.py test

# If the first argument is "logs"...
ifeq (logs,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "logs"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
logs:
	@docker-compose -f local.yml logs -f $(RUN_ARGS)

collectstatic:
	@docker-compose -f local.yml exec app python manage.py collectstatic --noinput

migrate:
	@docker-compose -f local.yml exec app python manage.py migrate

makemigrations:
	@docker-compose -f local.yml exec app python manage.py makemigrations

rm-volume:
	@make -s down
	@docker volume rm todo_example_postgres_data
