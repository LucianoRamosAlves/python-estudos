criar ambiente virtual

py -m venv .venv

ativar 
venv\Scripts\activate


desativar
deactivate

detro do ambient 
python -m pip install Django

python -m django --version

criar 
pip freeze > requirements.txt

para baixar as depedencias
pip install -r requirements.txt

baixar as configuraçoes 
django-admin startproject config .

migar o banco de dados 
python manage.py migrate

quando for fazer meu proprio tabela tem que fazer
python manage.py makemigrations

para rodar o servidor 
python manage.py runserver