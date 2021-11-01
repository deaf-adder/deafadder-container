import pytest

from deafadder_container.ContainerException import InstanceNotFound

from .deafadder_container_metatemplate_test_helper import _FirstDummyClassForTest, \
    _SecondDummyClassForTest, _InheritedComponentWithMetaclass, _InheritedComponentWithoutMetaclass


def test_delete_instance_success_when_instance_exist():
    _ = _FirstDummyClassForTest()
    _FirstDummyClassForTest.delete()


def test_delete_named_instance_success_when_instance_exist():
    _ = _FirstDummyClassForTest(instance_name="non default instance")
    _FirstDummyClassForTest.delete("non default instance")


def test_failure_delete_when_no_instance_exist():
    with pytest.raises(InstanceNotFound) as raised_exception:
        _FirstDummyClassForTest.delete()
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == "Unable to find an instance for " \
                                          "'<class 'deafadder_container.MetaTemplate.Component'>' with name 'default'"


def test_get_instance_fails_when_no_instance_exist():
    with pytest.raises(InstanceNotFound) as raised_exception:
        _ = _FirstDummyClassForTest.get()
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == "Unable to find an instance for " \
                                          "'<class 'deafadder_container.MetaTemplate.Component'>' " \
                                          "with name 'default'"


def test_get_instance_fails_when_no_instance_with_given_name():
    instance_first = _FirstDummyClassForTest()
    with pytest.raises(InstanceNotFound) as raised_exception:
        instance_second = _FirstDummyClassForTest.get("non default instance")
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == "Unable to find an instance for " \
                                          "'<class 'deafadder_container.MetaTemplate.Component'>' " \
                                          "with name 'non default instance'"

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
        _FirstDummyClassForTest.delete("non default instance")
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == "Unable to find an instance for " \
                                          "'<class 'deafadder_container.MetaTemplate.Component'>' " \
                                          "with name 'non default instance'"

    # Clean up
    _FirstDummyClassForTest.delete()


def test_can_create_instance_when_no_instance_exist_in_container():
    _ = _FirstDummyClassForTest()

    # Clean up
    _FirstDummyClassForTest.delete()


def test_can_create_instance_when_instance_of_other_class_exist_in_container():
    instance_first = _FirstDummyClassForTest()
    instance_second = _SecondDummyClassForTest()

    # Clean up
    _FirstDummyClassForTest.delete()
    _SecondDummyClassForTest.delete()


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

    instance_second = _FirstDummyClassForTest(instance_name="non default instance")
    assert instance_second.counter == 0
    instance_second.increment()
    assert instance_second.counter == 1

    assert instance_first != instance_second

    # Clean up
    _FirstDummyClassForTest.delete()
    _FirstDummyClassForTest.delete("non default instance")


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
    assert str(raised_exception.value) == "Unable to find an instance for " \
                                          "'<class 'deafadder_container.MetaTemplate.Component'>' " \
                                          "with name 'default'"

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
    assert str(raised_exception.value) == "Unable to find an instance for " \
                                          "'<class 'deafadder_container.MetaTemplate.Component'>' " \
                                          "with name 'default'"

    # Clean up
    _InheritedComponentWithMetaclass.delete()