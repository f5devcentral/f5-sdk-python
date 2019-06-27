# Introduction

This contains useful information about contributing to this project.

## Desgin Guidelines

In short this is the set of important rules to help contributors understand why the SDK is the way it is.

- Be consistent with industry standard SDK(s) - The goal is to make the SDK easy to understand...
- When in doubt, use keyword arguments - In general the point is to avoid making assumptions and think ahead
- [Semantic Versioning](https://semver.org) matters, this is critical to the user experience
- Keep the interfaces clean - Seperate management client from feature functionality client(s)
- Avoid creating hand-written documentation outside of the code to explain functionality at all costs - Doc strings exists, use them

## Scope

TBD

## Quality

- Testing exists, see [Test Readme](../tests/README.md)
- Code coverage, which is enforced: `coverage.py`
- Coding standards, which are enforced: `pylint`, `flake8`