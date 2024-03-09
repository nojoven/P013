import pytest
from users.templatetags.split_on_slash import split_on_slash
from django.test import TestCase


class TestSplitOnSlashFilter(TestCase):
    def test_split_on_slash(self):
        # Test avec une chaîne qui contient un slash
        self.assertEqual(split_on_slash("foo/bar"), "bar")

        # Test avec une chaîne qui ne contient pas de slash
        self.assertEqual(split_on_slash("foobar"), "foobar")

        # Test avec une chaîne vide
        self.assertEqual(split_on_slash(""), "")


# Parametrized test for happy path scenarios
@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        pytest.param("test/value", "value", id="single_slash"),
        pytest.param("test/multiple/slashes", "slashes", id="multiple_slashes"),
        pytest.param("no_slash", "no_slash", id="no_slash"),
        pytest.param("/leading_slash", "leading_slash", id="leading_slash"),
        pytest.param("trailing_slash/", "", id="trailing_slash"),
        pytest.param("//double/slash", "slash", id="double_slash"),
        pytest.param("", "", id="empty_string"),
    ],
)
def test_split_on_slash_happy_path(input_value, expected_output):
    # Act
    result = split_on_slash(input_value)

    # Assert
    assert result == expected_output


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        pytest.param(" ", " ", id="single_space"),
        pytest.param(" / ", " ", id="space_slash_space"),
        pytest.param("test/ value", " value", id="slash_space"),
        pytest.param("test//value", "value", id="consecutive_slashes"),
        pytest.param("test/value/", "", id="slash_at_end"),
    ],
)
def test_split_on_slash_edge_cases(input_value, expected_output):
    # Act
    result = split_on_slash(input_value)

    # Assert
    assert result == expected_output
