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
    else:
        return _is_one_ancestor_a_component(type(candidate))


def is_an_instance(candidate) -> bool:
    return isinstance(candidate, object)


def is_a_class(candidate) -> bool:
    return isinstance(candidate, type)
