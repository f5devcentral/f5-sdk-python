API_DOCS_SOURCE := ./docs/apidocs/source
BUILD_DIR := build
CODE_DOCS_DIR := ./code_docs
COVERAGE_DIR := ./code_coverage
COVERAGE_FILE := .coverage
DIST_DIR := dist
EGG_DIR := f5_cloud_sdk.egg-info
EXCLUDE_PATTERN := "*/abstract/*"
PACKAGE_DIR := f5cloudsdk
TEST_DIR := tests
UNIT_TEST_DIR := ${TEST_DIR}/unit
TEST_CACHE_DIR := .pytest_cache
EXAMPLES_DIR := examples

export SPHINX_APIDOC_OPTIONS = members,undoc-members,inherited-members

build:
	echo "Creating package artifacts";
	python3 setup.py sdist bdist_wheel;
unit_test:
	echo "Running unit tests";
	pytest ${UNIT_TEST_DIR} --cov=${PACKAGE_DIR} --full-trace -v;
lint:
	echo "Running linter (any error will result in non-zero exit code)";
	flake8 ${PACKAGE_DIR}/ ${EXAMPLES_DIR}/ ${TEST_DIR}/;
	pylint -j 0 ${PACKAGE_DIR}/ ${EXAMPLES_DIR}/ ${TEST_DIR}/;
coverage: unit_test
	echo "Generating code coverage documentation";
	coverage html;
code_docs:
	echo "Generating code documentation (via sphinx)";
	# auto generate sphinx API docs from package
	sphinx-apidoc --force --separate --module-first -o ${API_DOCS_SOURCE} ${PACKAGE_DIR} ${EXCLUDE_PATTERN};
	# make docs (html)
	cd docs && make html && cd ..;
	cp -R docs/_build ${CODE_DOCS_DIR};
code_docs_doxygen:
	echo "Generating code documentation (via doxygen)";
	doxygen doxygen.conf;
clean:
	echo "Removing artifacts"
	rm -rf ${API_DOCS_SOURCE}
	rm -rf ${BUILD_DIR}
	rm -rf ${CODE_DOCS_DIR}
	rm -rf ${COVERAGE_DIR}
	rm -rf ${COVERAGE_FILE}
	rm -rf ${DIST_DIR}
	rm -rf ${EGG_DIR}
	rm -rf ${TEST_CACHE_DIR}
.PHONY: clean
