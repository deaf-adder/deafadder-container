from .deafadder_container_metatemplate_test_helper import _FirstDummyClassForTest, _SecondDummyClassForTest


def test_can_create_instance_when_no_instance_exist_in_container():
    instance = _FirstDummyClassForTest()

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
