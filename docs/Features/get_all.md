# Get all

If you want to retrieve all the instances of a given `Component`, you can use 
the `Component.get_all(cls, pattern: str = None, names: List[str] = None)`.
It returns a dictionary where the key is the instance name and the value the actual instance. 

It takes two optional parameters: `pattern` and `names`. They are both used to have more granularity on which
instances we want to retrieve, based on their name.

* `pattern`: A string that contains a regex. It works exactly as the regular expression in `re.match`.
* `names`: A list of name that you want to retrieve.

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

With `pattern` and `names`: 
```python

if __name__ == "__main__":
    instance1 = MyComponent()
    instance2 = MyComponent(instance_name="non default 1")
    instance3 = MyComponent(instance_name="non default 2")
    instance4 = MyComponent(instance_name="non default 3")
    
    component_dict = Component.get_all(MyComponent, pattern=".* default [13]", names=["default"])
    
    assert "default" in component_dict
    assert "non default 1" in component_dict
    assert "non default 2" not in component_dict
    assert "non default 3" in component_dict
    
    assert len(component_dict) == 3
```