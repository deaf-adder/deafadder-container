# Testing

Several function exist that can help for testing. Of course, even though they were implemented with testing
purpose in mind, that does not exclude them from being used in non testing situation.

Those methods are mostly for deletion. Here, deleting mean being removed from the list of managed instances.
It will still exist in the application memory as long as another object hold a reference to it (like in dependency 
linked through autowire). For further details, have a look at the [memory model page](InDepth/memory-model.md)

For all the example below, let's assume we have the two following class:

```python
from deafadder_container.MetaTemplate import Component


class MyComponent(metaclass=Component):
    pass


class MyOtherComponent(metaclass=Component):
    pass
```

## `.delete(cls, instance_name: str = "default")`

To delete a single instance if you know the name of the instance.

```python
MyComponent()

assert MyComponent.get() is not None
assert Component.get(MyComponent) is not None

# or Component.delete(MyComponent)
MyComponent.delete()

# This instance does not exist anymore
try:
    MyComponent.get()
except InstanceNotFound:
    pass

```

And the same works with named instance:

```python
MyComponent(instance_name="non default")

assert MyComponent.get(instance_name="non default") is not None
assert Component.get(MyComponent, instance_name="non default") is not None

# or Component.delete(MyComponent, instance_name="non default")
MyComponent.delete(instance_name="non default")

# This instance does not exist anymore
try:
    MyComponent.get(instance_name="non default")
except InstanceNotFound:
    pass

```

## `.delete_all(cls)`

Delete all instance of a given class.

```python
MyComponent()
MyComponent(instance_name="non default")

assert MyComponent.get() is not None
assert MyComponent.get(instance_name="non default") is not None

# or Component.delete_all(MyComponent)
MyComponent.delete_all()

# The instances don't exist anymore
try:
    MyComponent.get()
except InstanceNotFound:
    pass

try:
    MyComponent.get(insance_name="non default")
except InstanceNotFound:
    pass

```

## `.purge()`

Delete all instance managed by the `Component` metaclass.

```python
MyComponent()
MyComponent(instance_name="non default")
MyOtherComponent()

assert MyComponent.get() is not None
assert MyComponent.get(instance_name="non default") is not None
assert MyOtherComponent.get() is not None

Component.purge()

# The instances don't exist anymore
try:
    MyComponent.get()
except InstanceNotFound:
    pass

try:
    MyComponent.get(insance_name="non default")
except InstanceNotFound:
    pass

try:
    MyOtherComponent.get(insance_name="non default")
except InstanceNotFound:
    pass

```
