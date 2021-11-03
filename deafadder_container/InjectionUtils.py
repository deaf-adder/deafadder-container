from deafadder_container.ContainerException import NotAContainer
from deafadder_container.DeafAdderUtils import assert_is_deafadder_container, is_an_instance, is_a_class


def inject(component, name: str = 'default'):
    assert_is_deafadder_container(component)
    if is_an_instance(component):
        return component.__class__.get(instance_name=name)
    if is_a_class(component):
        return component.get(instance_name=name)
    raise Exception # FIXME: use a proper Exception for unexpected behaviour (like, "this piece of code should not be reached"
