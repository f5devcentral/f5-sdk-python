# Introduction

This contains useful information about contributing to this project.

## Design Guidelines

In short this is the set of important rules to help contributors understand why the SDK is the way it is.

- Be consistent with industry standard SDK(s) - The goal is to make the SDK easy to understand...
- Keep the interfaces clean and simple
   - Seperate management client from feature functionality client(s)
- Each feature functionality client should support a single set of CRUD operations
- When in doubt, use keyword arguments - In general the point is to avoid making assumptions and think ahead
- [Semantic Versioning](https://semver.org) matters, this is critical to the user experience
- Avoid creating hand-written documentation outside of the code to explain functionality at all costs - Doc strings exists, use them
- CRUD operations should be provided using a consistent pattern
   - GET -> `list()` or `show()`
      - `list()`: If performing a `GET` on a collection of resources.
      - `show()`: If performing a `GET` on a single resource.
   - POST -> `create()`
   - PUT -> `update()`
   - DELETE -> `delete()`
- Prefer plural over singular for namespaces.  `from sdk import subscription` becomes `from sdk import subscriptions`

### SDK API

Below describes the SDK API given an example REST API definition which covers most common patterns.

- Given URI: `/device/pools/<a_pool>` - simple resource example
- And URI: `/device/pools/<a_pool>/members/<a_pool_member>` - child resource example
- And URI: `/device/pools/<a_pool>/poolview` - resource attribute leaf endpoint (typically GET only) example

```python
   from device import PoolsClient, PoolMembersClient

   # pool(s) level operations
   pools_client = PoolsClient()
   pools_client.list()
   pools_client.create(config={})
   pools_client.show(name='foo')
   pools_client.update(name='foo', config={})
   pools_client.delete(name='foo')
   pools_client.show_instance_view(name='foo')

   # pool member(s) level operations
   pool_members_client = PoolMembersClient(pool_name='foo')
   pool_members_client.list()
   pool_members_client.create(config={})
   pool_members_client.show(name='foo')
   pool_members_client.update(name='foo', config={})
   pool_members_client.delete(name='foo')
```

Pros:
- Keeps a given class focused on a single set of CRUD operations
- Parent resource identifiers only need to be provided during client instantiation

Cons:
- Requires creation of multiple client instances 


#### Alternate API Options

##### Alternate Option 1

```python
   from device import PoolsClient

   # pool(s) level operations
   pools_client = PoolsClient()
   pools_client.list()
   pools_client.create(config={})
   pools_client.show(name='foo')
   pools_client.update(name='foo', config={})
   pools_client.delete(name='foo')
   pools_client.show_instance_view(name='foo')

   # pool member(s) level operations
   pools_client.members.list(pool_name='foo')
   pools_client.members.create(pool_name='foo', config={})
   pools_client.members.show(pool_name='foo', name='foo')
   pools_client.members.update(pool_name='foo', name='foo', config={})
   pools_client.members.delete(pool_name='foo', name='foo')
```

Pros:
- Only need to create a single client instance

Cons:
- Invoking nested method requires passing values for all parent resource identifiers

##### Alternate Option 2

```python
   from device import PoolsClient

   # pool(s) level operations
   pools_client = PoolsClient()
   pools_client.list()
   pools_client.create(config={})
   pools_client.show(name='foo')
   pools_client.update(name='foo', config={})
   pools_client.delete(name='foo')
   pools_client.show_instance_view(name='foo')

   # pool member(s) level operations
   pools_client.list_members(pool_name='foo')
   pools_client.create_member(pool_name='foo', config={})
   pools_client.show_member(pool_name='foo', name='foo')
   pools_client.update_member(pool_name='foo', name='foo', config={})
   pools_client.delete_member(pool_name='foo', name='foo')
```

Pros:
- Only need to create a single client instance
- Keeps all public methods in the parent client instance

Cons:
- Invoking nested method requires passing values for all parent resource identifiers
- Design challenges when implementing for complex API could result in long method names


## Scope

- BIG-IP extension components
- BIG-IQ licensing API's
- F5 Cloud Services

## Quality

- Testing happens, see the [Test Readme](../tests/README.md) for more details.
- Code coverage is checked, and enforced: `coverage.py`
- Coding standards are enforced, using linters: `pylint`, `flake8`