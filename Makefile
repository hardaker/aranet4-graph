it:
	python3 setup.py build

package:
	rm -rf dist
	python3 setup.py sdist bdist_wheel

publish:
	python3 -m twine upload -u __token__ dist/*

install:
	python3 setup.py install
