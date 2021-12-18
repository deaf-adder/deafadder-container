import pytest

from deafadder_container.ContainerException import InstanceNotFound
from deafadder_container.MetaTemplate import Component, Scope

from .deafadder_container_metatemplate_test_helper import _FirstDummyClassForTest, \
    _SecondDummyClassForTest, _InheritedComponentWithMetaclass, _InheritedComponentWithoutMetaclass


DEFAULT = "default"
NON_DEFAULT_INSTANCE_NAME = "non default instance"


def instance_not_found_message(cls, name="default"):
    return f"Unable to find an instance for {cls} with name '{name}'"


def test_delete_instance_success_when_instance_exist():
    _ = _FirstDummyClassForTest()
    Component.delete(_FirstDummyClassForTest)


def test_delete_named_instance_success_when_instance_exist():
    _ = _FirstDummyClassForTest(instance_name=NON_DEFAULT_INSTANCE_NAME)
    Component.delete(_FirstDummyClassForTest, NON_DEFAULT_INSTANCE_NAME)


def test_failure_delete_when_no_instance_exist():
    with pytest.raises(InstanceNotFound) as raised_exception:
        Component.delete(_FirstDummyClassForTest)
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == instance_not_found_message(_FirstDummyClassForTest)


def test_get_instance_fails_when_no_instance_exist():
    with pytest.raises(InstanceNotFound) as raised_exception:
        _ = Component.get(_FirstDummyClassForTest)
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == instance_not_found_message(_FirstDummyClassForTest)


def test_get_instance_fails_when_no_instance_with_given_name():
    instance_first = _FirstDummyClassForTest()
    assert instance_first is not None
    with pytest.raises(InstanceNotFound) as raised_exception:
        _ = Component.get(_FirstDummyClassForTest, NON_DEFAULT_INSTANCE_NAME)
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == instance_not_found_message(_FirstDummyClassForTest, NON_DEFAULT_INSTANCE_NAME)

    # Clean up
    Component.delete(_FirstDummyClassForTest)


def test_get_instance_success_when_instance_exist():
    instance_first = _FirstDummyClassForTest()
    instance_second = Component.get(_FirstDummyClassForTest)

    assert instance_first == instance_second
    assert instance_first.counter == 0
    assert instance_second.counter == 0
    instance_first.increment()
    assert instance_first.counter == 1
    assert instance_second.counter == 1

    # Clean up
    Component.delete(_FirstDummyClassForTest)


def test_failure_delete_named_instance_when_name_no_component_with_given_name():
    _ = _FirstDummyClassForTest()
    with pytest.raises(InstanceNotFound) as raised_exception:
        Component.delete(_FirstDummyClassForTest, NON_DEFAULT_INSTANCE_NAME)
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == instance_not_found_message(_FirstDummyClassForTest, NON_DEFAULT_INSTANCE_NAME)

    # Clean up
    Component.delete(_FirstDummyClassForTest)


def test_can_create_instance_when_no_instance_exist_in_container():
    _ = _FirstDummyClassForTest()

    # Clean up
    Component.delete(_FirstDummyClassForTest)


def test_can_create_instance_when_instance_of_other_class_exist_in_container():
    instance_first = _FirstDummyClassForTest()
    instance_second = _SecondDummyClassForTest()

    assert instance_first is not None
    assert instance_second is not None

    # Clean up
    Component.delete(_FirstDummyClassForTest)
    Component.delete(_SecondDummyClassForTest)


def test_instance_is_not_unloaded_when_container_is_deleted():
    instance = _FirstDummyClassForTest()
    assert instance is not None
    assert instance.counter == 0

    Component.delete(_FirstDummyClassForTest)

    assert instance is not None
    assert instance.counter == 0
    instance.increment()
    assert instance.counter == 1

    with pytest.raises(InstanceNotFound):
        Component.delete(_FirstDummyClassForTest)


def test_created_new_instance_of_existing_class_in_container_return_existing_class():
    instance_first = _FirstDummyClassForTest()
    assert instance_first.counter == 0
    instance_first.increment()
    assert instance_first.counter == 1

    instance_second = _FirstDummyClassForTest()
    assert instance_second.counter == 1
    assert instance_second.counter == instance_first.counter
    assert instance_second == instance_first
    instance_second.increment()
    assert instance_first.counter == 2
    assert instance_second.counter == 2
    assert instance_first.counter == instance_second.counter

    # Clean up
    Component.delete(_FirstDummyClassForTest)


def test_can_create_new_instance_with_different_name():
    instance_first = _FirstDummyClassForTest()
    assert instance_first.counter == 0
    instance_first.increment()
    assert instance_first.counter == 1

    instance_second = _FirstDummyClassForTest(instance_name=NON_DEFAULT_INSTANCE_NAME)
    assert instance_second.counter == 0
    instance_second.increment()
    assert instance_second.counter == 1

    assert instance_first != instance_second

    # Clean up
    Component.delete(_FirstDummyClassForTest)
    Component.delete(_FirstDummyClassForTest, NON_DEFAULT_INSTANCE_NAME)


def test_object_without_explicit_metaclass_inheriting_from_component_container_are_singleton():
    instance_first = _InheritedComponentWithoutMetaclass()
    assert instance_first.counter == 0
    assert instance_first.second_counter == 0

    instance_second = _InheritedComponentWithoutMetaclass()
    assert instance_first.counter == 0
    assert instance_first.second_counter == 0

    assert instance_first is instance_second
    instance_first.increment()
    assert instance_first.counter == 1
    assert instance_first.second_counter == 1
    assert instance_second.counter == 1
    assert instance_second.counter == 1

    # Clean up
    Component.delete(_InheritedComponentWithoutMetaclass)


def test_inherited_component_without_explicit_metaclass_does_not_create_singleton_super_component():
    _ = _InheritedComponentWithoutMetaclass()
    with pytest.raises(InstanceNotFound) as raised_exception:
        Component.delete(_FirstDummyClassForTest)

    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == instance_not_found_message(_FirstDummyClassForTest)

    # Clean up
    Component.delete(_InheritedComponentWithoutMetaclass)


def test_object_with_explicit_metaclass_inheriting_from_component_container_are_singleton():
    instance_first = _InheritedComponentWithMetaclass()
    assert instance_first.counter == 0
    assert instance_first.second_counter == 0

    instance_second = _InheritedComponentWithMetaclass()
    assert instance_first.counter == 0
    assert instance_first.second_counter == 0

    assert instance_first is instance_second
    instance_first.increment()
    assert instance_first.counter == 1
    assert instance_first.second_counter == 1
    assert instance_second.counter == 1
    assert instance_second.counter == 1

    # Clean up
    Component.delete(_InheritedComponentWithMetaclass)


def test_inherited_component_with_explicit_metaclass_does_not_create_singleton_super_component():
    _ = _InheritedComponentWithMetaclass()
    with pytest.raises(InstanceNotFound) as raised_exception:
        Component.delete(_FirstDummyClassForTest)

    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == instance_not_found_message(_FirstDummyClassForTest)

    # Clean up
    Component.delete(_InheritedComponentWithMetaclass)


def test_delete_all_instance_of_same_class():
    instance_1 = _FirstDummyClassForTest()
    instance_2 = _FirstDummyClassForTest(instance_name="second")
    assert instance_1 is not None
    assert instance_2 is not None

    Component.delete_all(_FirstDummyClassForTest)

    with pytest.raises(InstanceNotFound) as first_raised:
        _ = _FirstDummyClassForTest.get()
    assert type(first_raised.value) is InstanceNotFound
    assert str(first_raised.value) == instance_not_found_message(_FirstDummyClassForTest)

    with pytest.raises(InstanceNotFound) as second_raised:
        _ = Component.get(_FirstDummyClassForTest)
    assert type(second_raised.value) is InstanceNotFound
    assert str(second_raised.value) == instance_not_found_message(_FirstDummyClassForTest)

    with pytest.raises(InstanceNotFound) as third_raised:
        _ = _FirstDummyClassForTest.get("second")
    assert type(third_raised.value) is InstanceNotFound
    assert str(third_raised.value) == instance_not_found_message(_FirstDummyClassForTest, "second")

    with pytest.raises(InstanceNotFound) as fourth_raised:
        _ = Component.get(_FirstDummyClassForTest, instance_name="second")
    assert type(fourth_raised.value) is InstanceNotFound
    assert str(fourth_raised.value) == instance_not_found_message(_FirstDummyClassForTest, "second")


def test_delete_all():
    instance1 = _FirstDummyClassForTest()
    instance2 = _FirstDummyClassForTest(instance_name="second")
    instance3 = _SecondDummyClassForTest()

    assert instance1 is not None
    assert instance2 is not None
    assert instance3 is not None

    Component.purge()

    with pytest.raises(InstanceNotFound) as first_raised:
        _ = _FirstDummyClassForTest.get()
    assert type(first_raised.value) is InstanceNotFound
    assert str(first_raised.value) == instance_not_found_message(_FirstDummyClassForTest)

    with pytest.raises(InstanceNotFound) as second_raised:
        _ = _FirstDummyClassForTest.get(instance_name="second")
    assert type(second_raised.value) is InstanceNotFound
    assert str(second_raised.value) == instance_not_found_message(_FirstDummyClassForTest, name="second")

    with pytest.raises(InstanceNotFound) as third_raised:
        _ = _SecondDummyClassForTest.get()
    assert type(third_raised.value) is InstanceNotFound
    assert str(third_raised.value) == instance_not_found_message(_SecondDummyClassForTest)


def test_delete_all_when_nothing_to_delete():
    _ = _FirstDummyClassForTest()
    # the first delete works because there are exising instances
    Component.delete_all(_FirstDummyClassForTest)

    # The second delete works as well since we don't raise error when deleting Component with no instances
    Component.delete_all(_FirstDummyClassForTest)

    with pytest.raises(InstanceNotFound) as raised:
        _ = _FirstDummyClassForTest.get()

    assert type(raised.value) is InstanceNotFound
    assert str(raised.value) == instance_not_found_message(_FirstDummyClassForTest)


def test_prototype_creation():
    prototype = _FirstDummyClassForTest(scope=Scope.PROTOTYPE)
    singleton = _FirstDummyClassForTest(scope=Scope.SINGLETON)

    assert prototype is not singleton
    prototype.increment()
    assert prototype.counter == 1
    assert singleton.counter == 0

    Component.purge()


class Base:

    name: str

    def __init__(self, name: str):
        self.name = name

    def echo(self):
        return f"hi, {self.name}"


def test_base():
    instance1 = Component.of(Base(name="Me"))
    instance2 = Component.of(Base(name="Not Me"))

    assert instance1.echo() == "hi, Me"
    assert instance2.echo() == "hi, Me"
