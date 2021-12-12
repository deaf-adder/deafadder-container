# Quick start

?> For full examples, a little more meaningful that the one below, head over [here](Example/basic.md)

?> For additional example, have a look inside the `tests` folder.


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
    my_component_retrieved = MyComponent.get()
    my_component_retrieved_bis = Component.get(MyComponent)
    assert my_component is my_component_retrieved
    assert my_component is my_component_retrieved_bis

```

