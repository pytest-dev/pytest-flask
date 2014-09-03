test:
	@py.test tests


clean:
	@rm -rf build dist *.egg-info
	@find . -name '*.py?' -delete
