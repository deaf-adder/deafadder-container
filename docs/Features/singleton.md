# Singleton(-ish)

Each class created with the `Component` metaclass are named singleton.

A named singleton is unique for a given name and class. That means that multiple instances
can exist at the same time given they have a different name.

By default, if the instance is not named when it is created, the name *default* will be given
to it. In the same way, when fetching an instance, if we don't provide a name to look for,
the methods will target the instance with the name *default*.

As long as you don't name your `Commponent` it will be true singleton.

## A basic singleton

```python
from deafadder_container.MetaTemplate import Component


class MyComponent(metaclass=Component):
    pass


if __name__ == "__main__":
    instance = MyComponent()

    # attempt to recreate it will return the existing instance
    instance_bis = MyComponent()
    assert instance is instance_bis

    # retrieving the instance will return the initial one
    instance_ter = MyComponent.get_component()
    assert instance is instance_ter

    instance_ter_bis = Component.get_component(MyComponent)
    assert instance is instance_ter_bis

    # creating an instance with the default name will return the initial one
    instance_quad = MyComponent(instance_name="default")
    assert instance is instance_quad

    # retrieving the instance with the name default will return the initial one
    instance_quint = MyComponent.get_component(instance_name="default")
    assert instance is instance_quint

    instance_quint_bis = Component.get_component(MyComponent, instance_name="default")
    assert instance is instance_quint_bis

```

## Named instances

```python
from deafadder_container.MetaTemplate import Component


class MyComponent(metaclass=Component):
    pass


if __name__ == "__main__":
    instance = MyComponent()
    named = MyComponent(instance_name="name")

    assert named is not instance

    # retrieving the named instance
    named_bis = MyComponent.get_component(instance_name="name")
    assert named is named_bis
    assert named is Component.get_component(MyComponent, instance_name="name")

    # creating an instance with the same name
    named_ter = MyComponent(instance_name="name")
    assert named is named_ter

```