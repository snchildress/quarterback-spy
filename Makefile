PYTHON_VERSION := $(shell python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

deploy:
	# Copy dependencies from the virtual env to the root 
	cp -r venv/lib/python$(PYTHON_VERSION)/site-packages/* .
	# Deploy the application
	serverless deploy
