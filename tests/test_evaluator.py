import pytest

from src.evaluator import evaluate


def test_precedence_multiplication_before_addition():
    assert evaluate("2 + 3 * 4") == 14.0


def test_precedence_division_before_subtraction():
    assert evaluate("10 - 6 / 2") == 7.0


def test_left_to_right_same_precedence():
    assert evaluate("10 - 4 - 3") == 3.0
    assert evaluate("100 / 5 / 2") == 10.0


def test_parentheses_override_precedence():
    assert evaluate("(2 + 3) * 4") == 20.0


def test_nested_parentheses():
    assert evaluate("((1 + 2) * (3 + 4)) / 7") == 3.0


def test_decimal_numbers():
    assert evaluate("2.5 * 4") == 10.0
    assert evaluate("0.1 + 0.2") == pytest.approx(0.3)


def test_unary_minus():
    assert evaluate("-3 + 5") == 2.0
    assert evaluate("2 * -(1 + 1)") == -4.0
    assert evaluate("-2 * 3") == -6.0


def test_whitespace_ignored():
    assert evaluate("  2\t+\n3  ") == 5.0
    assert evaluate(" ( 1 + 2 ) * ( 3 - 1 ) ") == 6.0


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate("1 / 0")
    with pytest.raises(ZeroDivisionError):
        evaluate("5 / (3 - 3)")


def test_empty_input_raises():
    with pytest.raises(ValueError):
        evaluate("")
    with pytest.raises(ValueError):
        evaluate("   ")


def test_unbalanced_parentheses_raise():
    with pytest.raises(ValueError):
        evaluate("(1 + 2")
    with pytest.raises(ValueError):
        evaluate("1 + 2)")


def test_consecutive_operators_raise():
    with pytest.raises(ValueError):
        evaluate("2 ++ * 3")
    with pytest.raises(ValueError):
        evaluate("2 + * 3")


def test_invalid_characters_raise():
    with pytest.raises(ValueError):
        evaluate("2 + a")
    with pytest.raises(ValueError):
        evaluate("abc")
    with pytest.raises(ValueError):
        evaluate("2 & 3")
