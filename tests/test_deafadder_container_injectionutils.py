import pytest

from deafadder_container.ContainerException import NotAContainer
from deafadder_container.DeafAdderUtils import assert_is_deafadder_container
from deafadder_container.MetaTemplate import Component


class _FirstDummyClassForTest(metaclass=Component):
    """This class is only use as a base class to test metaclass behaviour
    """

    counter: int

    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter = self.counter + 1


def test_exploration():
    a = _FirstDummyClassForTest()
    assert_is_deafadder_container(a)
    assert a is not None

    assert_is_deafadder_container(_FirstDummyClassForTest)

    _FirstDummyClassForTest.delete()


def test_exploration_bis():
    with pytest.raises(NotAContainer) as raised_exception:
        assert_is_deafadder_container(None)

    with pytest.raises(NotAContainer) as raised_exception:
        assert_is_deafadder_container(1)

    with pytest.raises(NotAContainer) as raised_exception:
        assert_is_deafadder_container("None")

    with pytest.raises(NotAContainer) as raised_exception:
        assert_is_deafadder_container(True)


def test_one():
    a = _FirstDummyClassForTest()
    assert_is_deafadder_container(a)
    assert_is_deafadder_container(_FirstDummyClassForTest)

    assert isinstance(a, object) is True
    assert isinstance(_FirstDummyClassForTest, type) is True

    _FirstDummyClassForTest.delete()