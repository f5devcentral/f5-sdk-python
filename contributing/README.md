# Introduction

This contains useful information about contributing to this project.

## Design Guidelines

In short this is the set of important rules to help contributors understand why the SDK is the way it is.

- Be consistent with industry standard SDK(s) - The goal is to make the SDK easy to understand...
- When in doubt, use keyword arguments - In general the point is to avoid making assumptions and think ahead
- [Semantic Versioning](https://semver.org) matters, this is critical to the user experience
- Keep the interfaces clean - Seperate management client from feature functionality client(s)
- Avoid creating hand-written documentation outside of the code to explain functionality at all costs - Doc strings exists, use them
- CRUD operations should be provided using a consistent pattern
   - GET -> `show()` or `list()` - If performing a `GET` on a single resource, use `show()`.  If the response is an array of resources, use `list()`.
   - POST -> `create()`
   - PUT -> `update()`
   - DELETE -> `delete()`

## Scope

- BIG-IP toolchain components
- F5 Cloud Services

## Quality

- Testing happens, see the [Test Readme](../tests/README.md) for more details.
- Code coverage is checked, and enforced: `coverage.py`
- Coding standards are enforced, using linters: `pylint`, `flake8`