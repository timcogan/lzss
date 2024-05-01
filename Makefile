PYTHON=pdm run python
PROJECT=lzss
LINE_LEN=120
CODE_DIRS=$(PROJECT) tests


test:
	$(PYTHON) -m coverage run --source $(PROJECT) -m pytest tests -s


style:
	$(PYTHON) -m autoflake -r -i $(CODE_DIRS)
	$(PYTHON) -m isort $(CODE_DIRS)
	$(PYTHON) -m autopep8 -a -r -i $(CODE_DIRS)
	$(PYTHON) -m black $(CODE_DIRS)


quality:
	$(PYTHON) -m black --check $(CODE_DIRS)
	$(PYTHON) -m flake8 --max-doc-length $(LINE_LEN) --max-line-length $(LINE_LEN) $(CODE_DIRS)


node_modules:
	npm install


types: node_modules
	pdm run npx --no-install pyright tests $(CODE_DIRS)


coverage:
	$(MAKE) test
	for command in xml report html ; do \
		$(PYTHON) -m coverage $$command --omit=$(PACKAGE_NAME)/version.py ; \
	done


check:
	$(MAKE) style
	$(MAKE) quality
	$(MAKE) types
	$(MAKE) coverage


pdm.lock:
	$(MAKE) update


update:
	pdm install -d


init: pdm.lock
	which pdm || pip install --user pdm
	pdm venv create -n $(PROJECT)
	pdm sync -d


clean:
	rm -rf \
		node_modules \
		env \
		*.egg-info \
		__pycache__
	pdm venv remove -y $(PROJECT)
	rm -f .pdm-python


reset:
	$(MAKE) clean
	$(MAKE) init
	$(MAKE) check


pypi:
	$(PYTHON) -m build
	$(PYTHON) -m twine upload dist/*