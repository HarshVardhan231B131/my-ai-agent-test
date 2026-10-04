"""Safe arithmetic expression evaluator.

A hand-written tokenizer and recursive descent parser for expressions
built from decimal numbers, the operators ``+``, ``-``, ``*``, ``/``
and parentheses.  ``eval()``, ``exec()`` and the ``ast`` module are
deliberately not used.

Grammar::

    expression := term { ("+" | "-") term }
    term       := factor { ("*" | "/") factor }
    factor     := ("+" | "-") factor | primary
    primary    := NUMBER | "(" expression ")"

Unary minus binds tighter than ``*`` and ``/`` (``-2 * 3 == -6``),
operators of equal precedence are evaluated left to right, and
whitespace is ignored anywhere in the expression.
"""

_WHITESPACE = " \t\r\n"
_OPERATORS = "+-*/"


class _Token:
    """A single lexical token produced by :func:`_tokenize`."""

    __slots__ = ("kind", "value")

    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f"_Token({self.kind!r}, {self.value!r})"


def _tokenize(expression):
    """Split *expression* into a list of tokens ending with an ``eof`` token."""
    tokens = []
    i = 0
    length = len(expression)
    while i < length:
        char = expression[i]
        if char in _WHITESPACE:
            i += 1
        elif char in _OPERATORS:
            tokens.append(_Token("op", char))
            i += 1
        elif char == "(":
            tokens.append(_Token("lparen", char))
            i += 1
        elif char == ")":
            tokens.append(_Token("rparen", char))
            i += 1
        elif char.isdigit() or char == ".":
            start = i
            seen_dot = False
            while i < length and (expression[i].isdigit() or expression[i] == "."):
                if expression[i] == ".":
                    if seen_dot:
                        raise ValueError(
                            f"invalid number {expression[start:i + 1]!r} at position {start}"
                        )
                    seen_dot = True
                i += 1
            text = expression[start:i]
            if text == ".":
                raise ValueError(f"invalid number '.' at position {start}")
            tokens.append(_Token("number", float(text)))
        else:
            raise ValueError(f"invalid character {char!r} at position {i}")
    tokens.append(_Token("eof", None))
    return tokens


class _Parser:
    """Recursive descent parser over the token list."""

    def __init__(self, tokens):
        self._tokens = tokens
        self._position = 0

    def _peek(self):
        return self._tokens[self._position]

    def _advance(self):
        token = self._tokens[self._position]
        self._position += 1
        return token

    def parse(self):
        value = self._expression()
        if self._peek().kind != "eof":
            raise ValueError(f"unexpected token {self._peek().value!r}")
        return value

    def _expression(self):
        value = self._term()
        while self._peek().kind == "op" and self._peek().value in ("+", "-"):
            operator = self._advance().value
            right = self._term()
            value = value + right if operator == "+" else value - right
        return value

    def _term(self):
        value = self._factor()
        while self._peek().kind == "op" and self._peek().value in ("*", "/"):
            operator = self._advance().value
            right = self._factor()
            if operator == "*":
                value *= right
            else:
                if right == 0:
                    raise ZeroDivisionError("division by zero")
                value /= right
        return value

    def _factor(self):
        token = self._peek()
        if token.kind == "op" and token.value in ("+", "-"):
            self._advance()
            operand = self._factor()
            return operand if token.value == "+" else -operand
        return self._primary()

    def _primary(self):
        token = self._advance()
        if token.kind == "number":
            return token.value
        if token.kind == "lparen":
            value = self._expression()
            closing = self._advance()
            if closing.kind != "rparen":
                raise ValueError("unbalanced parentheses: missing ')'")
            return value
        if token.kind == "eof":
            raise ValueError("unexpected end of expression")
        raise ValueError(f"unexpected token {token.value!r}")


def evaluate(expression):
    """Evaluate an arithmetic *expression* and return its value as a float.

    Supports ``+``, ``-``, ``*``, ``/``, parentheses, decimal numbers and
    unary minus.  Raises :class:`ZeroDivisionError` on division by zero and
    :class:`ValueError` for any malformed input (empty string, unbalanced
    parentheses, consecutive operators, unknown characters, ...).
    """
    if not isinstance(expression, str):
        raise ValueError("expression must be a string")
    return _Parser(_tokenize(expression)).parse()
