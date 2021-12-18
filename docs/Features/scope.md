# Scope

By default, each `Component` is treated as a singleton (ar at least a named instance is a singleton).

But if we want to take advantage of the autowiring mechanism without having to create a singleton (and hence not
having the new instance referenced somewhere for future fetching), you have to tell the scope of the `Component`.

There two scope for now: SINGLETON and PROTOTYPE. By default, the SINGLETON one is use.

## Example

```python
from deafadder_container.MetaTemplate import Component, Scope
from deafadder_container.ContainerException import InstanceNotFound


class InnerComponent(metaclass=Component):
    counter: int

    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter = self.counter + 1


class MyComponent(metaclass=Component):
    counter: int
    _inner_comp: InnerComponent

    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter = self.counter + 1
        self._inner_comp.increment()


if __name__ == "__main__":
    inner_comp = InnerComponent()

    comp_list = [MyComponent(scope=Scope.PROTOTYPE) for i in range(10)]

    # asserting all new instance are different
    for i in comp_list:
        for j in comp_list[1:]:
            assert i is not j

    for comp in comp_list:
        comp.increment()

    for comp in comp_list:
        assert comp.counter == 1

    assert inner_comp.counter == 10  # called 10 times with the self._inner_comp.increment()

    try:
        comp = MyComponent.get_component()
    except InstanceNotFound:
        print("There are Singleton instance of MyComponent that can be retrieved")

```

