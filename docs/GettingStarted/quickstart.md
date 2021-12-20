# Quick start

?> For additional example, have a look inside the `tests` folder or in the **Features** 
section of this documentation.


The most basic example is not fancy, but is enough to demonstrate a basic use case:

```python

from deafadder_container.MetaTemplate import Component


class MyComponent(metaclass=Component):
    token: str

    def __init__(self, token: str):
        self.token = token

    def show_my_token(self):
        print(self.token)


if __name__ == "__main__":
    my_component = MyComponent(token="token from config")

    # my_component is now a singleton
    my_component_bis = MyComponent()
    my_component_ter = MyComponent(token="other token")
    assert my_component is my_component_bis
    assert my_component is my_component_ter

    # but more importantly, it is retrievable
    # it can be accessed anywhere in the application with:
    my_component_retrieved = Component.get(MyComponent)
    assert my_component is my_component_retrieved

```

