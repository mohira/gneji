.PHONY: publish
publish:
	# poetry config http-basic.testpypi {{USER_NAME}} {{PASSWORD}}
	poetry build
	poetry publish -r testpypi
