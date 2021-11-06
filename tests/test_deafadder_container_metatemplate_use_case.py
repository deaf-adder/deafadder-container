import pytest

from deafadder_container.MetaTemplate import Component

from .deafadder_container_metatemplate_test_helper import _FirstDummyClassForTest, _CompositeDummyClassForTest, \
    _CompositeDummyClass2ForTest


@pytest.fixture
def first_dummy_component():
    yield _FirstDummyClassForTest()
    Component.delete(_FirstDummyClassForTest)


@pytest.fixture
def first_dummy_component_non_default():
    yield _FirstDummyClassForTest(instance_name="non default")
    Component.delete(_FirstDummyClassForTest, instance_name="non default")


def test_simple_composition(first_dummy_component):
    service = _CompositeDummyClassForTest()

    assert service.get_counter_value() == 0
    service.increment()
    assert service.get_counter_value() == 1

    first_dummy_component.increment()
    assert service.get_counter_value() == 2

    # Clean up
    Component.delete(_CompositeDummyClassForTest)


def test_intricate_composition(first_dummy_component):
    inner_service = _CompositeDummyClassForTest()
    service = _CompositeDummyClass2ForTest()

    assert service.get_counter_value() == 0
    service.increment()
    assert service.get_counter_value() == 1
    inner_service.increment()
    assert service.get_counter_value() == 2
    first_dummy_component.increment()
    assert service.get_counter_value() == 3

    # Clean up
    Component.delete(_CompositeDummyClassForTest)
    Component.delete(_CompositeDummyClass2ForTest)
