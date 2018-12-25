deploy:
	cp -r venv/lib/python3.6/site-packages/* .
	serverless deploy
