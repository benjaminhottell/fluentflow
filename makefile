# This makefile is not necessary for installing the project.


# Automatically creates a testing virtual environment
venv/test/.setup: makefile src/fluentflow/*.py
	mkdir -p venv
	python3 -m venv venv/test
	./venv/test/bin/pip3 install coverage mypy
	touch $@


# Automatically re-install the package as it is changed
venv/test/.install-fluentflow: venv/test/.setup src/fluentflow/*.py
	./venv/test/bin/pip3 install .
	touch $@


venv-test: venv/test/.setup venv/test/.install-fluentflow


# Automatically runs tests
test: venv-test
	./venv/test/bin/python3 -m mypy src
	./venv/test/bin/python3 -m mypy tests
	./venv/test/bin/python3 -m tests


clean:
	rm -r venv


.PHONY: test clean venv-test

