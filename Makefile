.PHONY: test clean docs publish


test:
	@py.test tests


clean:
	@rm -rf build dist *.egg-info
	@find . | grep -E '(__pycache__|\.pyc|\.pyo$$)' | xargs rm -rf


docs:
	sphinx-build docs docs/_build


publish:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel upload
