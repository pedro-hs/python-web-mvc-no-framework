coverage run --source=src/ -m unittest discover src/
coverage html --omit="*/env/*,*/test/*"
coverage report -m
