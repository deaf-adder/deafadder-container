# Post init

When creating a `Component`, it will undergo 3 steps:

1. applying `__init__` method if present.
2. inject other `Component` dependency through [autowiring](Features/autowire.md)
3. execute the `_post_init` method if present.

This mechanism is required when you'd like your `__init__` method to initialize your instance while using
a `Component` dependency. Since those are linked after the `__init__` execution, you can access any of those
field yet. But you can delegate the initialization part that need those dependency in the `_post_init` method.

## Example

```python
from deafadder_container.MetaTemplate import Component


class InnerComponent(metaclass=Component):
    
    def __init__(self, attr):
        self.attr = attr
    
    def printer(self):
        print(f"From InnerComponent: name='{self.attr}'")


class MyComponent(metaclass=Component):
    
    _inner_comp: InnerComponent

    def __init__(self):
        print("Here I can't use the _inner_comp field. It is not yet linked")

    def _post_init(self):
        print("Here I can use the _inner_compo field.")
        self._inner_comp.printer()


if __name__ == "__main__":
    InnerComponent(attr="my attribute")
    my_component = MyComponent()
```

after the `my_component = MyComponent()` call, it will print:

```
Here I can't use the _inner_comp field. It is not yet linked
Here I can use the _inner_compo field.
From InnerComponent: name='my attribute'
```