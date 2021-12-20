# Features

## Creation
* `MyCustomComponent(instance_name: str = "default", scope: Scope = Scope.SINGLETON, *args, **kwargs)`
* `Component.of(instance. instance_name: str = "default")`

## Retrieval
* `Component.get(cls, instance_name: str = "default")`. 
  * Return a single instance or raise an `InstanceNotFound` exception if no instance exist with the given name
  * Works for class that use the `Component` metaclass and normal class managed as a `Component`
* `MyCustomComponent.get_component(instance_name: str = "default")`. 
  * Return a single instance or raise an `InstanceNotFound` exception if no instance exist with the given name
  * Only works for class that use the `Component` metaclass
  * Can be called as `Component.get_component(cls, instance_name: str = "default")`
* `Component.get_all(cls)`.
  * Return a dictionary where the keys are the instance name and the values the actual instances.
  * Works for class that use the `Component` metaclass and normal class managed as a `Component`

## Deletion
* `MyCustomComponent.delete(instance_name: str = "default")`. 
  * Raise an `InstanceNotFound` exception if no instance exist with the given name
  * Only works for class that use the `Component` metaclass
  * Can be called as `Component.delete(cls, instance_name: str = "default")`
* `MyCustomComponent.delete_all(instance_name: str = "default")`. 
  * Only works for class that use the `Component` metaclass
  * Can be called as `Component.delete_all(cls, instance_name: str = "default")`
* `Component.purge()`
  * Works for class that use the `Component` metaclass and normal class managed as a `Component`
