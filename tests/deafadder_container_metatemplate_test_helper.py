from deafadder_container.MetaTemplate import Component


class _FirstDummyClassForTest(metaclass=Component):
    """This class is only use as a base class to test metaclass behaviour
    """

    counter: int

    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter = self.counter + 1


class _SecondDummyClassForTest(metaclass=Component):
    """This class is only use as a base class to test metaclass behaviour
    """

    counter: int

    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter = self.counter + 1


class _InheritedComponentWithMetaclass(_FirstDummyClassForTest, metaclass=Component):
    """This class is only use as a base class to test metaclass behaviour
    """

    second_counter: int

    def __init__(self):
        super().__init__()
        self.second_counter = 0

    def increment(self):
        self.counter = self.counter + 1
        self.second_counter = self.second_counter + 1


class _InheritedComponentWithoutMetaclass(_FirstDummyClassForTest):
    """This class is only use as a base class to test metaclass behaviour
    """

    second_counter: int

    def __init__(self):
        super().__init__()
        self.second_counter = 0

    def increment(self):
        self.counter = self.counter + 1
        self.second_counter = self.second_counter + 1


