python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r requirements.txt
python3.12 manage.py collectstatic --noinput
python3.12 manage.py migrate
