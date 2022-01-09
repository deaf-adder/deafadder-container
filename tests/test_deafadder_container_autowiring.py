from functools import wraps
from typing import List, Dict

import pytest

from deafadder_container.ContainerException import AnnotatedDeclarationMissing, MultipleAutowireReference, InstanceNotFound
from deafadder_container.MetaTemplate import Component
from deafadder_container.Wiring import autowire


@pytest.fixture(autouse=True)
def purge_component_fixture():
    yield
    Component.purge()


class _Dummy1(metaclass=Component):

    def get_one(self):
        return 1


class _Dummy2(metaclass=Component):

    a: int

    def get_two(self):
        return 2


class _Dummy3(metaclass=Component):

    service1: _Dummy1

    def get_three(self):
        return 3


class _Dummy4(metaclass=Component):

    service3: _Dummy3
    service4: _Dummy3
    service5: _Dummy3
    service6: _Dummy3

    def __init__(self):
        self.service3 = Component.get(_Dummy3)


class _Dummy5(metaclass=Component):
    service3: _Dummy3
    service4: _Dummy3
    service5: _Dummy3
    service6: _Dummy3

    @autowire(service5="non default 1", service6="non default 2")
    def __init__(self):
        self.service3 = Component.get(_Dummy3)


class _Dummy6(metaclass=Component):
    service3: _Dummy3
    service4: _Dummy3
    service5: _Dummy3
    service6: _Dummy3

    @autowire(service5="non default 1")
    @autowire(service6="non default 2")
    def __init__(self):
        self.service3 = Component.get(_Dummy3)


class _Dummy7(metaclass=Component):
    service3: _Dummy3
    service4: _Dummy3
    service5: _Dummy3
    service6: _Dummy3

    @autowire(service5="non default 1")
    @autowire(service7="non default 2")
    def __init__(self):
        self.service3 = Component.get(_Dummy3)


class _Dummy8(metaclass=Component):
    service3: _Dummy3
    service4: _Dummy3
    service5: _Dummy3
    service6: _Dummy3

    @autowire(service3="non default 1")
    @autowire(service5="non default 1")
    @autowire(service6="non default 2")
    def __init__(self):
        self.service3 = Component.get(_Dummy3)


class _Dummy9(metaclass=Component):
    service3: _Dummy3
    service4: _Dummy3
    service5: _Dummy3
    service6: _Dummy3

    @autowire(service5="non default 1", service6="non default 2")
    @autowire(service6="non default 2")
    def __init__(self):
        self.service3 = Component.get(_Dummy3)


class _Dummy10(_Dummy1):

    service1: _Dummy1
    service2: _Dummy2


class _Dummy11(_Dummy1):
    pass


class _Dummy12(_Dummy11):
    pass


class _Dummy13(metaclass=Component):

    service1: _Dummy12

    def get_thirteen(self):
        return 13


@pytest.fixture
def dummy1_default():
    yield _Dummy1()


@pytest.fixture
def dummy2_default():
    yield _Dummy2()


@pytest.fixture
def dummy3_default(dummy1_default):
    yield _Dummy3()


@pytest.fixture
def dummy3_non_default_1():
    yield _Dummy3(instance_name="non default 1")


@pytest.fixture
def dummy3_non_default_2():
    yield _Dummy3(instance_name="non default 2")


@pytest.fixture
def dummy10_default(dummy1_default, dummy2_default):
    yield _Dummy10()


@pytest.fixture
def dummy12_default():
    yield _Dummy12()


def test_default_autowire_for_non_set_annotated_component(dummy1_default):
    dummy3 = _Dummy3()

    assert dummy3.get_three() == 3
    assert dummy3.service1.get_one() == 1


def test_default_autowire_no_explicit_autowire_implicit_default(dummy3_default):
    dummy4 = _Dummy4()

    assert dummy4.service3.get_three() == 3
    assert dummy4.service4.get_three() == 3
    assert dummy4.service5.get_three() == 3
    assert dummy4.service6.get_three() == 3

    assert dummy4.service3 is dummy4.service4
    assert dummy4.service3 is dummy4.service5
    assert dummy4.service3 is dummy4.service6


def test_explicit_autowire_retrieve_correct_instance(dummy3_default, dummy3_non_default_1, dummy3_non_default_2):
    dummy5 = _Dummy5()

    assert dummy5.service3.get_three() == 3
    assert dummy5.service4.get_three() == 3
    assert dummy5.service5.get_three() == 3
    assert dummy5.service6.get_three() == 3

    assert dummy5.service3 is dummy5.service4
    assert dummy5.service3 is not dummy5.service5
    assert dummy5.service3 is not dummy5.service6


def test_explicit_autowire_with_multiple_decorator(dummy3_default, dummy3_non_default_1, dummy3_non_default_2):
    dummy6 = _Dummy6()

    assert dummy6.service3.get_three() == 3
    assert dummy6.service4.get_three() == 3
    assert dummy6.service5.get_three() == 3
    assert dummy6.service6.get_three() == 3

    assert dummy6.service3 is dummy6.service4
    assert dummy6.service3 is not dummy6.service5
    assert dummy6.service3 is not dummy6.service6


def test_explicit_autowire_cant_map_non_declared_annotated_component(dummy3_default, dummy3_non_default_1, dummy3_non_default_2):
    with pytest.raises(AnnotatedDeclarationMissing) as expected_raise:
        _ = _Dummy7()

    assert type(expected_raise.value) is AnnotatedDeclarationMissing
    assert str(expected_raise.value) == "Elements to autowire 'service7' should be defined and annotated at class level."


def test_explicit_autowire_try_to_override_already_set_component_fails(dummy3_default, dummy3_non_default_1, dummy3_non_default_2):
    with pytest.raises(AnnotatedDeclarationMissing) as expected_raise:
        _ = _Dummy8()

    assert type(expected_raise.value) is AnnotatedDeclarationMissing
    assert str(expected_raise.value) == "Elements to autowire 'service3' should be defined and annotated at class level."


def test_cant_explicit_autowire_multiple_time_the_same_field(dummy3_default, dummy3_non_default_1, dummy3_non_default_2):
    with pytest.raises(MultipleAutowireReference) as expected_raise:
        _ = _Dummy9()

    assert type(expected_raise.value) is MultipleAutowireReference
    assert str(expected_raise.value) == "The following arguments are referenced multiple times in autowire: service6"


def test_can_extend_and_require_same_dependency(dummy1_default, dummy2_default):

    dummy10 = _Dummy10()

    assert dummy10.get_one() == 1
    assert dummy10.service1.get_one() == 1
    assert dummy10.service2.get_two() == 2


def test_can_autowire_inherited_component(dummy12_default):
    dummy13 = _Dummy13()

    assert dummy13.get_thirteen() == 13
    assert dummy13.service1.get_one() == 1


class NormalClass:

    def __init__(self, attribute: str):
        self.attribute = attribute


class ComponentClass(metaclass=Component):

    normal_class_ref: NormalClass


def test_autowiring_with_component_of():
    normal_class_as_component = Component.of(NormalClass(attribute="my attribute"))
    component_instance = ComponentClass()

    assert normal_class_as_component is Component.of(NormalClass(attribute="something else"))
    assert normal_class_as_component is not Component.of(NormalClass(attribute="something else"), instance_name="non default")
    assert component_instance.normal_class_ref is normal_class_as_component

    assert component_instance.normal_class_ref.attribute == "my attribute"


class ComponentClassBis(metaclass=Component):

    normal_class_ref: NormalClass

    @autowire(normal_class_ref="non default")
    def __init__(self):
        pass


def test_autowiring_with_component_of_and_non_existing_named_instance():

    normal_class_as_component = Component.of(
        NormalClass(attribute="my attribute"),
        instance_name="default"
    )

    with pytest.raises(InstanceNotFound) as raised:
        _ = ComponentClassBis()

    assert type(raised.value) is InstanceNotFound
    assert str(raised.value) == f"Unable to find an instance for {normal_class_as_component.__class__} with name 'non default'"


def my_auto(**kwargs):
    """
    This decorator exist only to make sure the autowiring mechanism only take
    into account the "autowire" one

    :param kwargs:
    :return:
    """
    def decorator_autowire(init):
        @wraps(init)
        def wrapper_decorator(*init_args, **init_kwargs):
            instance = init(*init_args, **init_kwargs)
            return instance
        return wrapper_decorator
    return decorator_autowire

class ListAutowireClass(metaclass=Component):
    l: List[_Dummy3]
    d: Dict[str, _Dummy3]
    nl: _Dummy3

    @my_auto(l="", d="", nl="")
    @my_auto(l="", d="", nl="")
    @autowire(d=["non default 1", "default"], nl="non default 2")
    def __init__(self):
        pass


def test_list_autowire(dummy3_default, dummy3_non_default_1, dummy3_non_default_2):
    instance = ListAutowireClass()

    assert len(instance.l) == 3
    assert len(instance.d) == 2

    assert "non default 1" in instance.d
    assert "default" in instance.d