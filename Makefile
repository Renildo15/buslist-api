#formata o código
format:
	black .
	isort .
#roda as migrations
migrate:
	python manage.py makemigrations
	python manage.py migrate
#executa o servidor
server:
	python manage.py runserver

admin:
	python manage.py initadmin


#roda o docker-compose
db:
	docker compose up db
#instala as dependências
dependencies:
	pip install -r requirements.txt
#rodar os testes com o unittest
test_unittest:
	python manage.py test
#rodar os testes com o pytest
test_pytest:
	pytest
#rodar os testes com o pytest e gerar relatório de cobertura
coverage:
	coverage run -m pytest
	coverage report
	coverage html