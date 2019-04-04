# F5 Cloud SDK

## Table of Contents
- [Introduction](#introduction)
- [Quick Start](#quick-start)
- [Developer Setup](#developer-setup)
- [Artifacts](#artifacts)

## Introduction

...

## Quick Start

Note: Currently pulling from the develop branch

```bash
pip3 install f5-cloud-sdk --extra-index-url https://***REMOVED***/artifactory/api/pypi/f5-cloud-solutions-pypi/simple
```

Note: Alternatively install from local repo (any branch)

```bash
pip3 install .
```

## Developer Setup

### Installation

This is still a work in progress (no venv, etc.), however below are the current steps.

```bash
pip3 install -r requirements.txt
pip3 install .
```

### Testing

This project uses `Make` as a build automation tool... check out the Makefile for the full set of recipes.

- Run unit tests: ```make unit_test```
- Run linter: ```make lint```
- Build code coverage documentation: ```make coverage```
- Build code documentation: ```make docs```

## Artifacts

- Index: https://cloudsolutions.pages.***REMOVED***/f5-cloud-sdk
- Code coverage report: https://cloudsolutions.pages.***REMOVED***/f5-cloud-sdk/coverage/
- Code documentation: https://cloudsolutions.pages.***REMOVED***/f5-cloud-sdk/code-docs/

