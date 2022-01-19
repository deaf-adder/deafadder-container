# Delete

The `delete`, `delete_all` and `purge` functions were initially build with testing in mind. Of course, even though they 
were implemented for a testing purpose, that does not exclude them from being used in non testing situation.

Here, deleting mean being removed from the list of managed instances.
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

assert Component.get(MyComponent) is not None

# or Component.delete(MyComponent)
Component.delete(MyComponent)

# This instance does not exist anymore
try:
    Component.get(MyComponent)
except InstanceNotFound:
    pass

```

And the same works with named instance:

```python
MyComponent(instance_name="non default")

assert Component.get_component(MyComponent, instance_name="non default") is not None

# or Component.delete(MyComponent, instance_name="non default")
Component.delete(MyComponent, instance_name="non default")

# This instance does not exist anymore
try:
    Component.get(MyComponent, instance_name="non default")
except InstanceNotFound:
    pass

```

## `.delete_all(cls)`

Delete all or a subset of instance of a given class.

just as the [get_all](Features/get_all.md), you can target specific group of instances using `pattern`, `names` and `tags`.

```python
MyComponent()
MyComponent(instance_name="non default")

assert Component.get(MyComponent) is not None
assert Component.get(MyComponent, instance_name="non default") is not None

Component.delete_all(MyComponent)

# The instances don't exist anymore
try:
    Component.get(MyComponent)
except InstanceNotFound:
    pass

try:
    Component.get(MyComponent, insance_name="non default")
except InstanceNotFound:
    pass

```

or, using `pattern`, `names` and `tags`:

```python
instance1 = MyComponent(instance_name="name one")
instance2 = MyComponent(instance_name="name two")
instance3 = MyComponent(instance_name="Name three")
instance4 = MyComponent(instance_name="name four", tags=["first", "second"])
instance5 = MyComponent(instance_name="Name five", tags=["first", "third"])
instance6 = MyComponent(instance_name="name six", tags=["first", "fourth"])

# `pattern = "Name .*` will delete instance3, instance5
# `names=["name one", "Name three"]` will delete instance1, instance3
# `tags=["third", "fourth"]` will delete instance5, instance6
Component.delete_all(MyComponent, pattern="Name .*", names=["name one", "Name three"], tags=["third", "fourth"])

component_dict = Component.get_all(MyComponent)
assert len(component_dict) == 2
assert "name two" in component_dict and component_dict["name two"] is instance2
assert "name four" in component_dict and component_dict["name four"] is instance4
```

## `.purge()`

Delete all instance managed by the `Component` metaclass.

```python
MyComponent()
MyComponent(instance_name="non default")
MyOtherComponent()

assert Component.get(MyComponent) is not None
assert Component.get(MyComponent, instance_name="non default") is not None
assert Component.get(MyOtherComponent) is not None

Component.purge()

# The instances don't exist anymore
try:
    Component.get(MyComponent)
except InstanceNotFound:
    pass

try:
    Component.get(MyComponent, insance_name="non default")
except InstanceNotFound:
    pass

try:
    Component.get(MyOtherComponent, insance_name="non default")
except InstanceNotFound:
    pass

```
