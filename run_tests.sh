coverage run --source=src/ --omit="*/test/*,*/src/server.py" -m unittest discover .
coverage html --omit=src/test/,env/
coverage report -m
