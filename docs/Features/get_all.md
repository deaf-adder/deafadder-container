# Get all

If you want to retrieve all the instances of a given `Component`, you can use the `Component.get_all(cls)`.
It returns a dictionary where the key is the instance name and the value the actual instance. 

This method works as well for component create out of [normal class](Features/component-from-normal-class.md).

## Example

```python
from deafadder_container.MetaTemplate import Component


class MyComponent(metaclass=Component):
    pass


if __name__ == "__main__":
    instance1 = MyComponent()
    instance2 = MyComponent(instance_name="non default")
    instance3 = MyComponent(instance_name="another name")
    
    component_dict = Component.get_all(MyComponent)
    
    assert "default" in component_dict
    assert "non default" in component_dict
    assert "another name" in component_dict
    
    assert len(component_dict) == 3
```