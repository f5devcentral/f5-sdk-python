BUILD_DIR := build
CODE_DOCS_DIR := ./code_docs
COVERAGE_DIR := ./code_coverage
COVERAGE_FILE := .coverage
DIST_DIR := dist
EGG_DIR := f5_cloud_sdk.egg-info
PACKAGE_DIR := f5cloudsdk
TEST_DIR := tests
TEST_CACHE_DIR := .pytest_cache

build:
	echo "Creating package artifacts"
	python3 setup.py sdist bdist_wheel
unit_test:
	echo "Running unit tests";
	pytest --cov=${PACKAGE_DIR} ${TEST_DIR} -v;
lint:
	echo "Running linter (any error will result in non-zero exit code)";
	pylint ${PACKAGE_DIR}/;
coverage: unit_test
	echo "Generating code coverage documentation"
	coverage html
code_docs:
	echo "Generating code documentation (via sphinx)"
	# auto generate sphinx developer guide docs from package
	sphinx-apidoc --force --separate --module-first -o docs/developerguide/source ${PACKAGE_DIR}
	# make docs (html)
	cd docs && make html && cd ..
	cp -R docs/_build ${CODE_DOCS_DIR}
code_docs_doxygen:
	echo "Generating code documentation (via doxygen)"
	doxygen doxygen.conf
clean:
	echo "Removing artifacts"
	rm -rf ${BUILD_DIR}
	rm -rf ${CODE_DOCS_DIR}
	rm -rf ${COVERAGE_DIR}
	rm -rf ${COVERAGE_FILE}
	rm -rf ${DIST_DIR}
	rm -rf ${EGG_DIR}
	rm -rf ${TEST_CACHE_DIR}
.PHONY: clean
