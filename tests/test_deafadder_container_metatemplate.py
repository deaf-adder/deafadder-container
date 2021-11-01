import pytest

from deafadder_container.ContainerException import InstanceNotFound

from .deafadder_container_metatemplate_test_helper import _FirstDummyClassForTest, \
    _SecondDummyClassForTest, _InheritedComponentWithMetaclass, _InheritedComponentWithoutMetaclass


DEFAULT = "default"
NON_DEFAULT_INSTANCE_NAME = "non default instance"
ERROR_MESSAGE_FOR_INSTANCE_NOT_FOUND = "Unable to find an instance for " \
                                       "'<class 'deafadder_container.MetaTemplate.Component'>' with name '{}'"


def test_delete_instance_success_when_instance_exist():
    _ = _FirstDummyClassForTest()
    _FirstDummyClassForTest.delete()


def test_delete_named_instance_success_when_instance_exist():
    _ = _FirstDummyClassForTest(instance_name=NON_DEFAULT_INSTANCE_NAME)
    _FirstDummyClassForTest.delete(NON_DEFAULT_INSTANCE_NAME)


def test_failure_delete_when_no_instance_exist():
    with pytest.raises(InstanceNotFound) as raised_exception:
        _FirstDummyClassForTest.delete()
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == ERROR_MESSAGE_FOR_INSTANCE_NOT_FOUND.format(DEFAULT)


def test_get_instance_fails_when_no_instance_exist():
    with pytest.raises(InstanceNotFound) as raised_exception:
        _ = _FirstDummyClassForTest.get()
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == ERROR_MESSAGE_FOR_INSTANCE_NOT_FOUND.format(DEFAULT)


def test_get_instance_fails_when_no_instance_with_given_name():
    instance_first = _FirstDummyClassForTest()
    assert instance_first is not None
    with pytest.raises(InstanceNotFound) as raised_exception:
        _ = _FirstDummyClassForTest.get(NON_DEFAULT_INSTANCE_NAME)
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == ERROR_MESSAGE_FOR_INSTANCE_NOT_FOUND.format(NON_DEFAULT_INSTANCE_NAME)

    # Clean up
    _FirstDummyClassForTest.delete()


def test_get_instance_success_when_instance_exist():
    instance_first = _FirstDummyClassForTest()
    instance_second = _FirstDummyClassForTest.get()

    assert instance_first == instance_second
    assert instance_first.counter == 0
    assert instance_second.counter == 0
    instance_first.increment()
    assert instance_first.counter == 1
    assert instance_second.counter == 1

    # Clean up
    _FirstDummyClassForTest.delete()


def test_failure_delete_named_instance_when_name_no_component_with_given_name():
    _ = _FirstDummyClassForTest()
    with pytest.raises(InstanceNotFound) as raised_exception:
        _FirstDummyClassForTest.delete(NON_DEFAULT_INSTANCE_NAME)
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == ERROR_MESSAGE_FOR_INSTANCE_NOT_FOUND.format(NON_DEFAULT_INSTANCE_NAME)

    # Clean up
    _FirstDummyClassForTest.delete()


def test_can_create_instance_when_no_instance_exist_in_container():
    _ = _FirstDummyClassForTest()

    # Clean up
    _FirstDummyClassForTest.delete()


def test_can_create_instance_when_instance_of_other_class_exist_in_container():
    instance_first = _FirstDummyClassForTest()
    instance_second = _SecondDummyClassForTest()

    assert instance_first is not None
    assert instance_second is not None

    # Clean up
    _FirstDummyClassForTest.delete()
    _SecondDummyClassForTest.delete()


def test_instance_is_not_unloaded_when_container_is_deleted():
    instance = _FirstDummyClassForTest()
    assert instance is not None
    assert instance.counter == 0

    _FirstDummyClassForTest.delete()

    assert instance is not None
    assert instance.counter == 0
    instance.increment()
    assert instance.counter == 1

    with pytest.raises(InstanceNotFound):
        _FirstDummyClassForTest.delete()


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
    _FirstDummyClassForTest.delete()


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
    _FirstDummyClassForTest.delete()
    _FirstDummyClassForTest.delete(NON_DEFAULT_INSTANCE_NAME)


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
    _InheritedComponentWithoutMetaclass.delete()


def test_inherited_component_without_explicit_metaclass_does_not_create_singleton_super_component():
    _ = _InheritedComponentWithoutMetaclass()
    with pytest.raises(InstanceNotFound) as raised_exception:
        _FirstDummyClassForTest.delete()

    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == ERROR_MESSAGE_FOR_INSTANCE_NOT_FOUND.format(DEFAULT)

    # Clean up
    _InheritedComponentWithoutMetaclass.delete()


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
    _InheritedComponentWithMetaclass.delete()


def test_inherited_component_with_explicit_metaclass_does_not_create_singleton_super_component():
    _ = _InheritedComponentWithMetaclass()
    with pytest.raises(InstanceNotFound) as raised_exception:
        _FirstDummyClassForTest.delete()

    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == ERROR_MESSAGE_FOR_INSTANCE_NOT_FOUND.format(DEFAULT)

    # Clean up
    _InheritedComponentWithMetaclass.delete()
