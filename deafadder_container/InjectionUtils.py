import functools
import inspect

from deafadder_container.ContainerException import UnexpectedStatement, NotAContainerInstance
from deafadder_container.DeafAdderUtils import assert_is_deafadder_container, is_an_instance, is_a_class


class _WiringDescriptor:

    def __init__(self, target_type, container_name: str = "default"):
        assert_is_deafadder_container(target_type)
        if is_a_class(target_type):
            self.target_type = target_type
        self.container_name = container_name


def _get_wiring_members(instance) -> list:
    assert_is_deafadder_container(instance)
    if not is_an_instance(instance):
        raise NotAContainerInstance(f"The given instance '{instance}' is not a valid instance")
    _members = inspect.getmembers(instance, lambda member: not (inspect.isroutine(member)))

    members = [
        {
            "name": m[0],
            "member": m[1],
            "actual": getattr(instance, m[0])
        }
        for m in _members if type(m[1]) is _WiringDescriptor
    ]
    return members


def wiring(target_type, container_name: str = "default"):
    return _WiringDescriptor(target_type, container_name)


def autowire(cls):

    @functools.wraps(cls)
    def wrapper_autowire(*args, **kwargs):
        instance = cls(*args, **kwargs)
        attributes = _get_wiring_members(instance)
        for a in attributes:
            setattr(
                instance,
                a["name"],
                a["actual"].target_type.get(a["actual"].container_name))
        return instance

    return wrapper_autowire


def inject(component, name: str = 'default'):
    assert_is_deafadder_container(component)
    if is_an_instance(component):
        return component.__class__.get(instance_name=name)
    if is_a_class(component):
        return component.get(instance_name=name)
    raise UnexpectedStatement
