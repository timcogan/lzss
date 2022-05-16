PY_VER=python3.10
PY_VER_SHORT=py$(shell echo $(PY_VER) | sed 's/[^0-9]*//g')
VENV=env
PYTHON=$(VENV)/bin/python3
COVERAGE=$(VENV)/bin/coverage
PACKAGE_NAME=lz77
TEST_FOLDER=tests
CODE_DIRS=$(PACKAGE_NAME) $(TEST_FOLDER) util.py setup.py
LINE_LEN=120


test: $(VENV)
	$(COVERAGE) run --source $(PACKAGE_NAME) -m pytest $(TEST_FOLDER) $(CIRCLECI_TEST_FLAGS) -s


style: $(VENV)
	$(PYTHON) -m autoflake -r -i --remove-all-unused-imports --remove-unused-variables $(CODE_DIRS)
	$(PYTHON) -m isort $(CODE_DIRS) --line-length $(LINE_LEN) 
	$(PYTHON) -m autopep8 -a -r -i --max-line-length=$(LINE_LEN) $(CODE_DIRS) 
	$(PYTHON) -m black --line-length $(LINE_LEN) --target-version $(PY_VER_SHORT) $(CODE_DIRS)


quality: $(VENV)
	$(PYTHON) -m black --check --line-length $(LINE_LEN) --target-version $(PY_VER_SHORT) $(CODE_DIRS)
	$(PYTHON) -m flake8 --max-line-length $(LINE_LEN) $(CODE_DIRS) 


node_modules:
	npm install


types: node_modules
	npx --no-install pyright $(CODE_DIRS) -p pyrightconfig.json


coverage:
	$(MAKE) test
	for command in xml report html ; do \
		$(COVERAGE) $$command --omit=$(PACKAGE_NAME)/version.py ; \
	done


check:
	$(MAKE) style
	$(MAKE) quality
	$(MAKE) types
	$(MAKE) coverage


$(VENV):
	git submodule update --init --recursive
	python3 -m virtualenv -p $(PY_VER) $(VENV)
	$(PYTHON) -m pip install --upgrade pip==20.0.2
	$(PYTHON) -m pip install wheel
	$(PYTHON) -m pip install -r requirements.txt


init:
	$(MAKE) $(VENV)


clean:
	rm -rf \
		node_modules \
		env \
		*.egg-info \
		__pycache__


reset:
	$(MAKE) clean
	$(MAKE) check
