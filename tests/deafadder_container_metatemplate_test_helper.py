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


class _CompositeDummyClassForTest(metaclass=Component):

    base_service: _FirstDummyClassForTest

    def __init__(self):
        self.base_service = Component.get(_FirstDummyClassForTest)

    def get_counter_value(self):
        return self.base_service.counter

    def increment(self):
        self.base_service.increment()


class _CompositeDummyClass2ForTest(metaclass=Component):

    base_service: _FirstDummyClassForTest
    composite_service: _CompositeDummyClassForTest

    def __init__(self):
        self.base_service = Component.get(_FirstDummyClassForTest)
        self.composite_service = Component.get(_CompositeDummyClassForTest)

    def get_counter_value(self):
        return self.base_service.counter

    def increment(self):
        self.base_service.increment()


class _CompositeDummyClassWithNamedComponentForTest(metaclass=Component):

    base_service: _FirstDummyClassForTest

    def __init__(self):
        self.base_service = Component.get(_FirstDummyClassForTest, "non default")

    def get_counter_value(self):
        return self.base_service.counter

    def increment(self):
        self.base_service.increment()


class _CompositeDummyClass3ForTest(metaclass=Component):

    base_service: _FirstDummyClassForTest
    counter = None

    def __init__(self):
        self.counter_at_creation = 0

    def _post_init(self):
        self.base_service.increment()
        self.counter = self.base_service.counter
