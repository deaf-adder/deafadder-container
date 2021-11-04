class DeafAdderContainerException(Exception):
    pass


class InstanceNotFound(DeafAdderContainerException):
    pass


class NotAContainer(DeafAdderContainerException):
    pass


class NotAContainerInstance(NotAContainer):
    pass



class UnexpectedStatement(DeafAdderContainerException):
    pass