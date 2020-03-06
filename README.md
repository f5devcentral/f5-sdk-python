# F5 SDK

## Table of Contents
- [Introduction](#introduction)
- [Documentation](#documentation)
- [Developer Setup](#developer-setup)
- [Artifacts](#artifacts)

## Introduction

The F5 SDK Python provides client libraries to access various F5 products and services. It will focus primarily on facilitating consuming our most popular APIs and services, currently including BIG-IP (via Automation Tool Chain) and F5 Cloud Services. 

Benefits: 

- Provides hand-written or auto-generated client code to make F5’s APIs/services simple and intuitive to use.  
- Handles the low-level details of communication with the API or service, including authentication sessions, async task handling, protocol handling, large file uploads and more.  
- Can be installed using familiar package management tools such as pip. 


## Documentation

See the [user documentation](https://clouddocs.f5.com/sdk/f5-sdk-python/) for details on installation, usage and much more.

## Developer Setup

During development, F5 recommends using the specific pinned dependencies, including test dependencies, defined inside of requirements.txt instead of a production installation via `setup.py`.

### Installation

Note: A virtual environment should be created first.  See [python docs](https://docs.python.org/3/library/venv.html) for more details.

```bash
pip install -r requirements.txt && pip install .
```

Note: This project prefers Python 3.x, however if testing against python 2.x you should use either:

- A virtual environment
- Python 2.7 in a container - `docker run --rm -it -v $(pwd):/usr/dir python:2.7 /bin/bash`

### Testing

This project uses `Make` as a build automation tool... check out the Makefile for the full set of recipes.

- Run unit tests: ```make test```
- Run linter: ```make lint```
- Build code coverage documentation: ```make coverage```
- Build code documentation: ```make code_docs```

## Artifacts

- Index: https://automation-sdk.pages.***REMOVED***/f5-sdk-python
- Code coverage report: https://automation-sdk..pages.***REMOVED***/f5-sdk-python/coverage/
- Code documentation: https://automation-sdk..pages.***REMOVED***/f5-sdk-python/code-docs/
