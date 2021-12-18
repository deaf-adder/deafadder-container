# Component from normal class

You can create a `Component` out of a normal class (a class that does not use the `Component` metaclass) in order to make this class available for
injection through `autowire` for simply to create a singleton.

To do so, you hae to use the `Component.of(instance)` where instance is the actual instance of the object you want to convert to a `Component`.

## Example

```python
from deafadder_container.MetaTemplate import Component

class NormalClass:
    
    def __init__(self, attribute: str):
        self.attribute = attribute

        
class ComponentClass(metaclass=Component):

    normal_class_ref: NormalClass
    
    

if __name__ == "__main__":
    normal_class_as_component = Component.of(NormalClass(attribute="my attribute"))
    component_instance = ComponentClass()
    
    assert normal_class_as_component is Component.of(NormalClass(attribute="something else"))
    assert normal_class_as_component is not Component.of(NormalClass(attribute="something else"), instance_name="non default")
    assert component_instance.normal_class_ref is normal_class_as_component
    
    assert component_instance.normal_class_ref.attribute == "my attribute"

```