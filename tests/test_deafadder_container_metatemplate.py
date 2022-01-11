import pytest

from deafadder_container.ContainerException import InstanceNotFound
from deafadder_container.MetaTemplate import Component, Scope

from .deafadder_container_metatemplate_test_helper import _FirstDummyClassForTest, \
    _SecondDummyClassForTest, _InheritedComponentWithMetaclass, _InheritedComponentWithoutMetaclass


DEFAULT = "default"
NON_DEFAULT_INSTANCE_NAME = "non default instance"


@pytest.fixture
def purge():
    yield
    Component.purge()


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


def test_get_instance_fails_when_no_instance_with_given_name(purge):
    instance_first = _FirstDummyClassForTest()
    assert instance_first is not None
    with pytest.raises(InstanceNotFound) as raised_exception:
        _ = Component.get(_FirstDummyClassForTest, NON_DEFAULT_INSTANCE_NAME)
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == instance_not_found_message(_FirstDummyClassForTest, NON_DEFAULT_INSTANCE_NAME)


def test_get_instance_success_when_instance_exist(purge):
    instance_first = _FirstDummyClassForTest()
    instance_second = Component.get(_FirstDummyClassForTest)
    instance_third = Component.get(_FirstDummyClassForTest)
    instance_fourth = Component.get(_FirstDummyClassForTest)

    assert instance_first == instance_second
    assert instance_first.counter == 0
    assert instance_second.counter == 0
    instance_first.increment()
    assert instance_first.counter == 1
    assert instance_second.counter == 1

    assert instance_first is instance_second
    assert instance_first is instance_third
    assert instance_first is instance_fourth


def test_failure_delete_named_instance_when_name_no_component_with_given_name(purge):
    _ = _FirstDummyClassForTest()
    with pytest.raises(InstanceNotFound) as raised_exception:
        Component.delete(_FirstDummyClassForTest, NON_DEFAULT_INSTANCE_NAME)
    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == instance_not_found_message(_FirstDummyClassForTest, NON_DEFAULT_INSTANCE_NAME)


def test_can_create_instance_when_no_instance_exist_in_container(purge):
    _ = _FirstDummyClassForTest()


def test_can_create_instance_when_instance_of_other_class_exist_in_container(purge):
    instance_first = _FirstDummyClassForTest()
    instance_second = _SecondDummyClassForTest()

    assert instance_first is not None
    assert instance_second is not None


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


def test_created_new_instance_of_existing_class_in_container_return_existing_class(purge):
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


def test_can_create_new_instance_with_different_name(purge):
    instance_first = _FirstDummyClassForTest()
    assert instance_first.counter == 0
    instance_first.increment()
    assert instance_first.counter == 1

    instance_second = _FirstDummyClassForTest(instance_name=NON_DEFAULT_INSTANCE_NAME)
    assert instance_second.counter == 0
    instance_second.increment()
    assert instance_second.counter == 1

    assert instance_first != instance_second


def test_object_without_explicit_metaclass_inheriting_from_component_container_are_singleton(purge):
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


def test_inherited_component_without_explicit_metaclass_does_not_create_singleton_super_component(purge):
    _ = _InheritedComponentWithoutMetaclass()
    with pytest.raises(InstanceNotFound) as raised_exception:
        Component.delete(_FirstDummyClassForTest)

    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == instance_not_found_message(_FirstDummyClassForTest)


def test_object_with_explicit_metaclass_inheriting_from_component_container_are_singleton(purge):
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


def test_inherited_component_with_explicit_metaclass_does_not_create_singleton_super_component(purge):
    _ = _InheritedComponentWithMetaclass()
    with pytest.raises(InstanceNotFound) as raised_exception:
        Component.delete(_FirstDummyClassForTest)

    assert type(raised_exception.value) is InstanceNotFound
    assert str(raised_exception.value) == instance_not_found_message(_FirstDummyClassForTest)


def test_delete_all_instance_of_same_class():
    instance_1 = _FirstDummyClassForTest()
    instance_2 = _FirstDummyClassForTest(instance_name="second")
    assert instance_1 is not None
    assert instance_2 is not None

    Component.delete_all(_FirstDummyClassForTest)

    with pytest.raises(InstanceNotFound) as first_raised:
        _ = Component.get(_FirstDummyClassForTest)
    assert type(first_raised.value) is InstanceNotFound
    assert str(first_raised.value) == instance_not_found_message(_FirstDummyClassForTest)

    with pytest.raises(InstanceNotFound) as second_raised:
        _ = Component.get(_FirstDummyClassForTest)
    assert type(second_raised.value) is InstanceNotFound
    assert str(second_raised.value) == instance_not_found_message(_FirstDummyClassForTest)

    with pytest.raises(InstanceNotFound) as third_raised:
        _ = Component.get(_FirstDummyClassForTest, "second")
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
        _ = Component.get(_FirstDummyClassForTest)
    assert type(first_raised.value) is InstanceNotFound
    assert str(first_raised.value) == instance_not_found_message(_FirstDummyClassForTest)

    with pytest.raises(InstanceNotFound) as second_raised:
        _ = Component.get(_FirstDummyClassForTest, instance_name="second")
    assert type(second_raised.value) is InstanceNotFound
    assert str(second_raised.value) == instance_not_found_message(_FirstDummyClassForTest, name="second")

    with pytest.raises(InstanceNotFound) as third_raised:
        _ = Component.get(_SecondDummyClassForTest)
    assert type(third_raised.value) is InstanceNotFound
    assert str(third_raised.value) == instance_not_found_message(_SecondDummyClassForTest)


def test_delete_all_when_nothing_to_delete():
    _ = _FirstDummyClassForTest()
    # the first delete works because there are exising instances
    Component.delete_all(_FirstDummyClassForTest)

    # The second delete works as well since we don't raise error when deleting Component with no instances
    Component.delete_all(_FirstDummyClassForTest)

    with pytest.raises(InstanceNotFound) as raised:
        _ = Component.get(_FirstDummyClassForTest)

    assert type(raised.value) is InstanceNotFound
    assert str(raised.value) == instance_not_found_message(_FirstDummyClassForTest)


def test_prototype_creation(purge):
    prototype = _FirstDummyClassForTest(scope=Scope.PROTOTYPE)
    singleton = _FirstDummyClassForTest(scope=Scope.SINGLETON)

    assert prototype is not singleton
    prototype.increment()
    assert prototype.counter == 1
    assert singleton.counter == 0


class Base:

    name: str

    def __init__(self, name: str):
        self.name = name

    def echo(self):
        return f"hi, {self.name}"


def test_base(purge):
    instance1 = Component.of(Base(name="Me"))
    instance2 = Component.of(Base(name="Not Me"))

    assert instance1.echo() == "hi, Me"
    assert instance2.echo() == "hi, Me"

    assert instance1 is instance2


def test_get_all_for_component_when_component_exist(purge):

    instance_first_1 = _FirstDummyClassForTest()
    instance_first_2 = _FirstDummyClassForTest(instance_name="non default")
    instance_second_1 = _SecondDummyClassForTest()

    component_dict = Component.get_all(_FirstDummyClassForTest)

    assert len(component_dict) == 2
    assert component_dict["default"] is instance_first_1
    assert component_dict["non default"] is instance_first_2
    assert instance_second_1 not in component_dict.values()


def test_get_all_for_component_when_no_component_exist():

    component_dict = Component.get_all(_FirstDummyClassForTest)

    assert len(component_dict) == 0


def test_get_all_for_normal_class_as_component_when_existing(purge):
    instance_base_1 = Component.of(Base(name="Me"))
    instance_base_2 = Component.of(Base(name="Not me"), instance_name="non default")
    instance_first_1 = _FirstDummyClassForTest()

    component_dict = Component.get_all(Base)

    assert len(component_dict) == 2
    assert component_dict["default"] == instance_base_1
    assert component_dict["non default"] == instance_base_2
    assert instance_first_1 not in component_dict.values()


def test_delete_for_normal_class_as_component(purge):
    Component.of(Base(name="Me"))
    Component.of(Base(name="Not me"), instance_name="non default")

    assert len(Component.get_all(Base)) == 2

    Component.delete(Base)

    assert len(Component.get_all(Base)) == 1
    with pytest.raises(InstanceNotFound) as raised:
        Component.get(Base)
    assert str(raised.value) == instance_not_found_message(Base, name="default")

    # this one does not raise an exception
    Component.get(Base, "non default")


def test_delete_all_for_normal_class_as_component():
    Component.of(Base(name="Me"))
    Component.of(Base(name="Not me"), instance_name="non default")

    assert len(Component.get_all(Base)) == 2

    Component.delete_all(Base)

    assert len(Component.get_all(Base)) == 0

    with pytest.raises(InstanceNotFound) as first_raised:
        Component.get(Base)
    assert str(first_raised.value) == instance_not_found_message(Base, name="default")

    with pytest.raises(InstanceNotFound) as second_raised:
        Component.get(Base, instance_name="non default")
    assert str(second_raised.value) == instance_not_found_message(Base, name="non default")


def test_get_all_with_list_name_when_some_match(purge):
    instance_1 = _FirstDummyClassForTest(instance_name="non default 1")
    _ = _FirstDummyClassForTest(instance_name="non default 2")
    instance_3 = _FirstDummyClassForTest(instance_name="non default 3")

    instances = Component.get_all(_FirstDummyClassForTest, names=["non default 1", "non default 3"])

    assert len(instances) == 2

    assert "non default 1" in instances
    assert instances["non default 1"] is instance_1

    assert "non default 2" not in instances

    assert "non default 3" in instances
    assert instances["non default 3"] is instance_3


def test_get_all_with_list_name_when_none_match(purge):
    _1 = _FirstDummyClassForTest(instance_name="non default 1")  # noqa: F841
    _2 = _FirstDummyClassForTest(instance_name="non default 2")  # noqa: F841
    _3 = _FirstDummyClassForTest(instance_name="non default 3")  # noqa: F841

    instances = Component.get_all(_FirstDummyClassForTest, names=["Non default 1", "default 3"])

    assert len(instances) == 0


def test_get_all_with_pattern_name_when_some_match(purge):
    instance_1 = _FirstDummyClassForTest(instance_name="non default 1")
    _ = _FirstDummyClassForTest(instance_name="non default 2")
    instance_3 = _FirstDummyClassForTest(instance_name="non default 3")

    instances = Component.get_all(_FirstDummyClassForTest, pattern=".*[13]")

    assert len(instances) == 2

    assert "non default 1" in instances
    assert instances["non default 1"] is instance_1

    assert "non default 2" not in instances

    assert "non default 3" in instances
    assert instances["non default 3"] is instance_3


def test_get_all_with_pattern_name_when_none_match(purge):
    _1 = _FirstDummyClassForTest(instance_name="non default 1")  # noqa: F841
    _2 = _FirstDummyClassForTest(instance_name="non default 2")  # noqa: F841
    _3 = _FirstDummyClassForTest(instance_name="non default 3")  # noqa: F841

    instances = Component.get_all(_FirstDummyClassForTest, pattern="Non DEFAULT [1-3]")

    assert len(instances) == 0


def test_get_all_with_name_and_pattern_when_some_match_with_no_overlap(purge):
    instance_1 = _FirstDummyClassForTest(instance_name="non default 1")
    _ = _FirstDummyClassForTest(instance_name="non default 2")
    instance_3 = _FirstDummyClassForTest(instance_name="non default 3")
    instance_4 = _FirstDummyClassForTest(instance_name="Non Default 4")

    instances = Component.get_all(_FirstDummyClassForTest, names=["non default 1"], pattern="[Nn]on [Dd]efault [3-4]")

    assert len(instances) == 3

    assert "non default 1" in instances
    assert instances["non default 1"] is instance_1

    assert "non default 2" not in instances

    assert "non default 3" in instances
    assert instances["non default 3"] is instance_3

    assert "Non Default 4" in instances
    assert instances["Non Default 4"] is instance_4


def test_get_all_with_name_and_pattern_when_some_match_with_overlap(purge):
    instance_1 = _FirstDummyClassForTest(instance_name="non default 1")
    _ = _FirstDummyClassForTest(instance_name="non default 2")
    instance_3 = _FirstDummyClassForTest(instance_name="non default 3")
    instance_4 = _FirstDummyClassForTest(instance_name="Non Default 4")

    instances = Component.get_all(_FirstDummyClassForTest, names=["non default 1"], pattern="[Nn]on [Dd]efault [134]")

    assert len(instances) == 3

    assert "non default 1" in instances
    assert instances["non default 1"] is instance_1

    assert "non default 2" not in instances

    assert "non default 3" in instances
    assert instances["non default 3"] is instance_3

    assert "Non Default 4" in instances
    assert instances["Non Default 4"] is instance_4


def test_get_all_with_name_and_pattern_when_none_match(purge):
    _1 = _FirstDummyClassForTest(instance_name="non default 1")  # noqa: F841
    _2 = _FirstDummyClassForTest(instance_name="non default 2")  # noqa: F841
    _3 = _FirstDummyClassForTest(instance_name="non default 3")  # noqa: F841

    instances = Component.get_all(_FirstDummyClassForTest, pattern="Non DEFAULT [1-3]", names=["non default 4", "non default 5"])

    assert len(instances) == 0


def test_get_all_with_tags(purge):
    instance_1 = _FirstDummyClassForTest(instance_name="one", tags=["first", "second"])
    instance_2 = _FirstDummyClassForTest(instance_name="two", tags=["second", "third"])
    _ = _FirstDummyClassForTest(instance_name="three", tags=["third", "fourth"])
    instance_4 = _FirstDummyClassForTest(instance_name="four", tags=["fourth", "fifth", "sixth"])

    instances = Component.get_all(_FirstDummyClassForTest, tags=["second", "sixth"])

    assert len(instances) == 3

    assert "one" in instances
    assert instances["one"] is instance_1

    assert "two" in instances
    assert instances["two"] is instance_2

    assert "three" not in instances

    assert "four" in instances
    assert instances["four"] is instance_4


def test_delete_all_with_name_when_some_match(purge):
    _1 = _FirstDummyClassForTest(instance_name="one")  # noqa: F841
    _2 = _FirstDummyClassForTest(instance_name="two")  # noqa: F841
    instance_3 = _FirstDummyClassForTest(instance_name="three")

    Component.delete_all(_FirstDummyClassForTest, names=["one", "two"])

    with pytest.raises(InstanceNotFound):
        Component.get(_FirstDummyClassForTest, "one")

    with pytest.raises(InstanceNotFound):
        Component.get(_FirstDummyClassForTest, "two")

    assert Component.get(_FirstDummyClassForTest, "three") is instance_3
    assert len(Component.get_all(_FirstDummyClassForTest)) == 1


def test_delete_all_with_name_when_none_match(purge):
    instance_1 = _FirstDummyClassForTest(instance_name="one")
    instance_2 = _FirstDummyClassForTest(instance_name="two")
    instance_3 = _FirstDummyClassForTest(instance_name="three")

    Component.delete_all(_FirstDummyClassForTest, names=["four"])

    assert len(Component.get_all(_FirstDummyClassForTest)) == 3
    assert Component.get(_FirstDummyClassForTest, "one") is instance_1
    assert Component.get(_FirstDummyClassForTest, "two") is instance_2
    assert Component.get(_FirstDummyClassForTest, "three") is instance_3


def test_delete_all_with_pattern_when_some_match(purge):
    _1 = _FirstDummyClassForTest(instance_name="default one")  # noqa: F841
    _2 = _FirstDummyClassForTest(instance_name="default two")  # noqa: F841
    instance_3 = _FirstDummyClassForTest(instance_name="DEFAULT three")

    Component.delete_all(_FirstDummyClassForTest, pattern="default .*")

    with pytest.raises(InstanceNotFound):
        Component.get(_FirstDummyClassForTest, "default one")

    with pytest.raises(InstanceNotFound):
        Component.get(_FirstDummyClassForTest, "default two")

    assert Component.get(_FirstDummyClassForTest, "DEFAULT three") is instance_3
    assert len(Component.get_all(_FirstDummyClassForTest)) == 1


def test_delete_all_with_pattern_when_none_match(purge):
    instance_1 = _FirstDummyClassForTest(instance_name="default one")
    instance_2 = _FirstDummyClassForTest(instance_name="default two")
    instance_3 = _FirstDummyClassForTest(instance_name="DEFAULT three")

    Component.delete_all(_FirstDummyClassForTest, pattern="Default .*")

    assert len(Component.get_all(_FirstDummyClassForTest)) == 3
    assert Component.get(_FirstDummyClassForTest, "default one") is instance_1
    assert Component.get(_FirstDummyClassForTest, "default two") is instance_2
    assert Component.get(_FirstDummyClassForTest, "DEFAULT three") is instance_3


def test_delete_all_with_tags_when_some_match(purge):
    _1 = _FirstDummyClassForTest(instance_name="one", tags=["one", "two"])  # noqa: F841
    _2 = _FirstDummyClassForTest(instance_name="two", tags=["two", "three"])  # noqa: F841
    instance_3 = _FirstDummyClassForTest(instance_name="three", tags=["three", "four"])

    Component.delete_all(_FirstDummyClassForTest, tags=["two"])

    with pytest.raises(InstanceNotFound):
        Component.get(_FirstDummyClassForTest, "one")

    with pytest.raises(InstanceNotFound):
        Component.get(_FirstDummyClassForTest, "two")

    assert Component.get(_FirstDummyClassForTest, "three") is instance_3
    assert len(Component.get_all(_FirstDummyClassForTest)) == 1


def test_delete_all_with_tags_when_none_match(purge):
    instance_1 = _FirstDummyClassForTest(instance_name="one", tags=["one", "two"])
    instance_2 = _FirstDummyClassForTest(instance_name="two", tags=["two", "three"])
    instance_3 = _FirstDummyClassForTest(instance_name="three", tags=["three", "four"])

    Component.delete_all(_FirstDummyClassForTest, tags=["five"])

    assert len(Component.get_all(_FirstDummyClassForTest)) == 3
    assert Component.get(_FirstDummyClassForTest, "one") is instance_1
    assert Component.get(_FirstDummyClassForTest, "two") is instance_2
    assert Component.get(_FirstDummyClassForTest, "three") is instance_3
