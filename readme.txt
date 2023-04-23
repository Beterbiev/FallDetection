python -m venv myvenv
myvenv\scripts\activate
flask run --host=0.0.0.0

set FLASK_APP=main.py
set FLASK_DEBUG=1