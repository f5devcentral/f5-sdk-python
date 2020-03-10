API_DOCS_SOURCE := ./docs/apidocs/source
PKG_BUILD_DIR := f5_sdk_python.egg-info
CODE_DOCS_DIR := ./code_docs
CODE_DOCS_BUILD_DIR := docs/_build
COVERAGE_DIR := ./code_coverage
COVERAGE_FILE := .coverage
DIST_DIR := dist
BUILD_DIR := build
EGG_DIR := f5_sdk.egg-info
EXCLUDE_PATTERN := "*/abstract/*"
PACKAGE_DIR := f5sdk
TEST_DIR := tests
UNIT_TEST_DIR := ${TEST_DIR}/unit
FUNCTIONAL_TEST_DIR := ${TEST_DIR}/functional
TEST_CACHE_DIR := .pytest_cache
EXAMPLES_DIR := examples
EXTENSION_METADATA_FILE := metadata.json

export SPHINX_APIDOC_OPTIONS = members,undoc-members,inherited-members

build:
	echo "Creating package artifacts";
	python3 setup.py sdist bdist_wheel;
test:
	echo "Running unit tests";
	pytest ${UNIT_TEST_DIR} --cov=${PACKAGE_DIR} --full-trace -vv;
functional-test:
	echo "Running functional tests (behave.ini file for settings)";
	behave
functional-test-examples:
	echo "Running examples functional tests";
	pytest ${FUNCTIONAL_TEST_DIR}/examples --full-trace -vv;
lint:
	echo "Running linter (any error will result in non-zero exit code)";
	pylint -j 0 ${PACKAGE_DIR}/ ${EXAMPLES_DIR}/ ${TEST_DIR}/;
coverage: test
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
generate_extension_metadata:
	python3 -m "f5sdk.scripts.extension.generate_metadata";
	cp ${EXTENSION_METADATA_FILE} f5sdk/bigip/extension/extension_metadata.json
upload: build
	echo "Uploading package to PyPI";
	# set username/password using TWINE_USERNAME/TWINE_PASSWORD
	# or using keyring for automated scenarios
	twine check ${DIST_DIR}/*
	twine upload --skip-existing ${DIST_DIR}/*
clean:
	echo "Removing artifacts"
	rm -rf ${API_DOCS_SOURCE}
	rm -rf ${PKG_BUILD_DIR}
	rm -rf ${CODE_DOCS_DIR}
	rm -rf ${CODE_DOCS_BUILD_DIR}
	rm -rf ${COVERAGE_DIR}
	rm -rf ${COVERAGE_FILE}
	rm -rf ${DIST_DIR}
	rm -rf ${EGG_DIR}
	rm -rf ${TEST_CACHE_DIR}
	rm -rf ${BUILD_DIR}
clean_cache:
	find . -type d -name __pycache__ -exec rm -r {} \+
.PHONY: clean
