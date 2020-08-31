coverage run --source=src/ --omit="*/test/*" -m unittest discover src/
coverage html --omit=src/test/,env/
coverage report -m
