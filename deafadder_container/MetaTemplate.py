from dataclasses import dataclass
from threading import Lock
from typing import Any, Dict, List
from deafadder_container.ContainerException import InstanceNotFound


DEFAULT_INSTANCE_NAME = "default"


@dataclass
class _NamedInstance:
    name: str
    instance: Any


class Component(type):

    _instances: Dict[Any, List[_NamedInstance]] = {}
    _lock: Lock = Lock()

    def __call__(cls, instance_name: str = DEFAULT_INSTANCE_NAME, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = []
            if instance_name not in cls._known_instance_name_for_class():
                new_instance = super().__call__(*args, **kwargs)
                cls._instances[cls].append(_NamedInstance(name=instance_name, instance=new_instance))
        container_entry = cls._get_entry_for_name(instance_name)
        return container_entry.instance

    def get(cls, instance_name: str = DEFAULT_INSTANCE_NAME):
        if cls in cls._instances and instance_name in cls._known_instance_name_for_class():
            return cls._get_entry_for_name(instance_name).instance
        else:
            raise InstanceNotFound(f"Unable to find an instance for '{type(cls)}' with name '{instance_name}'")

    def delete(cls, instance_name: str = DEFAULT_INSTANCE_NAME):
        with cls._lock:
            if cls in cls._instances and instance_name in cls._known_instance_name_for_class():
                cls._instances[cls] = list(filter(lambda i: i.name != instance_name, cls._instances[cls]))
            else:
                raise InstanceNotFound(f"Unable to find an instance for '{type(cls)}' with name '{instance_name}'")

    def delete_all(cls):
        with cls._lock:
            if cls in cls._instances:
                cls._instances.pop(cls)

    def _known_instance_name_for_class(cls) -> List[str]:
        return [i.name for i in cls._instances[cls]]

    def _get_entry_for_name(cls, instance_name) -> _NamedInstance:
        return next(filter(lambda i: i.name == instance_name, cls._instances[cls]))
