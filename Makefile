BUILD_DIR := build
DIST_DIR := dist
EGG_DIR := f5_cloud_sdk.egg-info
PACKAGE_DIR := f5cloudsdk
TEST_DIR := tests
COVERAGE_DIR := ./code_coverage
COVERAGE_FILE := .coverage

build:
	echo "Creating package artifacts"
	python3 setup.py sdist bdist_wheel
unit_test:
	echo "Running unit tests (incl code coverage)";
	pytest --cov=${PACKAGE_DIR} ${TEST_DIR}/;
	coverage html
lint:
	echo "Running linter (any error will result in non-zero exit code)";
	pylint ${PACKAGE_DIR}/;
clean:
	echo "Removing artifacts"
	rm -rf ${BUILD_DIR}
	rm -rf ${DIST_DIR}
	rm -rf ${EGG_DIR}
	rm -rf ${COVERAGE_DIR}
	rm -rf ${COVERAGE_FILE}
.PHONY: clean
