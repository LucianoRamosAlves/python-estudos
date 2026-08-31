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