import pytest
import logging

from deafadder_container.ContainerException import InstanceNotFound
from deafadder_container.MetaTemplate import Component, Scope

from .deafadder_container_metatemplate_test_helper import _FirstDummyClassForTest, _CompositeDummyClassForTest, \
    _CompositeDummyClass2ForTest, _CompositeDummyClass3ForTest


@pytest.fixture(autouse=True)
def purge():
    yield
    Component.purge()


@pytest.fixture
def first_dummy_component():
    yield _FirstDummyClassForTest()


@pytest.fixture
def first_dummy_component_non_default():
    yield _FirstDummyClassForTest(instance_name="non default")


def test_simple_composition(first_dummy_component):
    service = _CompositeDummyClassForTest()

    assert service.get_counter_value() == 0
    service.increment()
    assert service.get_counter_value() == 1

    first_dummy_component.increment()
    assert service.get_counter_value() == 2


def test_simple_composition_fails_with_prototype_reference():
    _ = _FirstDummyClassForTest(scope=Scope.PROTOTYPE)
    with pytest.raises(InstanceNotFound) as raised:
        _ = _CompositeDummyClassForTest()

    assert type(raised.value) is InstanceNotFound
    assert str(raised.value) == "Unable to find an instance for " \
                                "<class 'tests.deafadder_container_metatemplate_test_helper._FirstDummyClassForTest'> " \
                                "with name 'default'"


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


def test_logging(caplog):
    Component.purge()

    with caplog.at_level(logging.DEBUG):
        _ = _FirstDummyClassForTest()
        assert len(caplog.records) == 4

        expected_message = [
            "(__call__ <class 'tests.deafadder_container_metatemplate_test_helper._FirstDummyClassForTest'>, default) Component not present, "
            "initializing the entry in the instance record.",

            "(__call__ <class 'tests.deafadder_container_metatemplate_test_helper._FirstDummyClassForTest'>, default) No instance with name "
            "'default' found for the Component. Creating it...",

            "(_AutowireMechanism.apply <class 'tests.deafadder_container_metatemplate_test_helper._FirstDummyClassForTest'>, default) "
            "Nothing to inject",

            "(__call__ <class 'tests.deafadder_container_metatemplate_test_helper._FirstDummyClassForTest'>, default) Instance found."
        ]

        for record, expected in zip(caplog.records, expected_message):
            assert record.message == expected


def test_post_init(first_dummy_component):
    instance = _CompositeDummyClass3ForTest()

    assert instance.counter == 1
    assert first_dummy_component.counter == 1
    first_dummy_component.increment()

    assert instance.counter == 1
    assert first_dummy_component.counter == 2
