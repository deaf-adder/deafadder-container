# Features

## Creation
* `MyCustomComponent(instance_name: str = "default", scope: Scope = Scope.SINGLETON, *args, **kwargs)`
* `Component.of(instance, instance_name: str = "default")`
  * create a `Component` out of a normal class.

## Retrieval
* `Component.get(cls, instance_name: str = "default")`
  * Retrieve a `Component` by it's class and it's name.
  * Return a single instance or raise an `InstanceNotFound` exception if no instance exist with the given name.
  * Works for class that use the `Component` metaclass and normal class managed as a `Component`.
* `Component.get_all(cls)`
  * Retrieve all the `Component` of a given class.
  * Return a dictionary where the keys are the instance name and the values the actual instances.
  * Works for class that use the `Component` metaclass and normal class managed as a `Component`.

## Deletion
* `Component.delete(cls: str = "default")`
  * Delete a `Component` based on it's class and name.
  * Raise an `InstanceNotFound` exception if no instance exist with the given name .
  * Works for class that use the `Component` metaclass and normal class managed as a `Component`.
* `Component.delete_all(cls, instance_name: str = "default")`
  * Delete all the `Component` of the given class.
  * Works for class that use the `Component` metaclass and normal class managed as a `Component`.
* `Component.purge()`
  * Delete all `Component`.
  * Works for class that use the `Component` metaclass and normal class managed as a `Component`.
