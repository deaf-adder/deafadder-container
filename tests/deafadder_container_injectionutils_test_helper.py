from typing import Any, cast

import pytest

from deafadder_container.ContainerException import NotAContainer
from deafadder_container.DeafAdderUtils import assert_is_deafadder_container
from deafadder_container.InjectionUtils import wiring, autowire
from deafadder_container.MetaTemplate import Component


class _BaseDummyClassForTest(metaclass=Component):
    """This class is only use as a base class to test metaclass behaviour
    """

    counter: int

    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter = self.counter + 1


@autowire
class _CompositeDummyClassForTest(metaclass=Component):

    base_service = wiring(_BaseDummyClassForTest)

    def get_counter_value(self):
        return self.base_service.counter

    def increment(self):
        self.base_service.increment()


@autowire
class _CompositeDummyClass2ForTest(metaclass=Component):

    base_service = wiring(_BaseDummyClassForTest)
    composite_service = wiring(_CompositeDummyClassForTest)

    def get_counter_value(self):
        return self.base_service.counter

    def increment(self):
        self.base_service.increment()


@autowire
class _CompositeDummyClassWithNamedComponentForTest(metaclass=Component):
    base_service = wiring(_BaseDummyClassForTest, "non default")

    def get_counter_value(self):
        return self.base_service.counter

    def increment(self):
        self.base_service.increment()