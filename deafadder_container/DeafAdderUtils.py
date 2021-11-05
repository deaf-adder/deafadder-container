import types

from deafadder_container.ContainerException import NotAContainer
from deafadder_container.MetaTemplate import Component


def assert_is_deafadder_container(candidate):
    if not _is_one_ancestor_a_component(candidate):
        raise NotAContainer("")


def _is_one_ancestor_a_component(candidate) -> bool:
    if type(candidate) is type:
        return False
    if type(candidate) is Component:
        return True
    if isinstance(candidate, types.FunctionType):
        components_full_name = [f'{c.__module__}.{c.__name__}' for c in Component._instances]
        if f'{candidate.__module__}.{candidate.__name__}' in components_full_name:
            return True
    else:
        return _is_one_ancestor_a_component(type(candidate))


def is_an_instance(candidate) -> bool:
    return isinstance(candidate, object)


def is_a_class(candidate) -> bool:
    return isinstance(candidate, type)
