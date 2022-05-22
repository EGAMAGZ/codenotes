from codenotes import Annotations


def test_annotation_that_exist():
    assert Annotations.get_value_by_key("task") != -1
    assert Annotations.get_value_by_key("TaSk") != -1


def test_annotation_that_not_exist():
    assert Annotations.get_value_by_key("homwework") == -1
