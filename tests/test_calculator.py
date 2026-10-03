from src.calculator import add, multiply, subtract


def test_add():
    assert add(2, 3) == 5


def test_multiply():
    assert multiply(2, 3) == 6


def test_multiply_negative():
    assert multiply(-2, 3) == -6


def test_multiply_zero():
    assert multiply(0, 5) == 0


def test_subtract():
    assert subtract(5, 3) == 2
