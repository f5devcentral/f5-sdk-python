PACKAGE_DIR := f5cloudsdk
TEST_DIR := tests
COVERAGE_DIR := ./coverage_html
COVERAGE_FILE := .coverage

unit_test:
	echo "Running unit tests (incl code coverage)";
	pytest --cov=${PACKAGE_DIR} ${TEST_DIR}/;
	coverage html
clean:
	echo "Removing artifacts"
	rm -rf ${COVERAGE_DIR}
	rm -rf ${COVERAGE_FILE}
.PHONY: clean
