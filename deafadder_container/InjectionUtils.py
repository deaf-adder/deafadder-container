from deafadder_container.ContainerException import NotAContainer
from deafadder_container.DeafAdderUtils import assert_is_deafadder_container, is_an_instance, is_a_class


def inject(component, name: str = 'default'):
    assert_is_deafadder_container(component)
    if is_an_instance(component):
        return component.__class__.get(instance_name=name)
    if is_a_class(component):
        return component.get(instance_name=name)
    raise Exception # FIXME: use a proper Exception for unexpected behaviour (like, "this piece of code should not be reached"




class ContainerDescriptor:

    def __init__(self, target_type, container_name: str = "default"):
        assert_is_deafadder_container(target_type)
        if is_a_class(target_type):
            self.target_type = target_type
        self.container_name = container_name


def wiring(target_type, container_name: str = "default"):
    return ContainerDescriptor(target_type, container_name)
