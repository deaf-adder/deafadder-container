class DeafAdderContainerException(Exception):
    pass


class InstanceNotFound(DeafAdderContainerException):
    pass


class NotAContainer(DeafAdderContainerException):
    pass