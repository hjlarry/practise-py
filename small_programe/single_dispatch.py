from functools import singledispatch
from collections import abc
import numbers
import html
import fractions
import decimal


@singledispatch
def htmlize(obj: object) -> str:
    content = html.escape(repr(obj))
    return f"<pre>{content}</pre>"


# Python 3.7以后可以直接用type hint决定 single_dispatch的类型
@htmlize.register
def _(text: str) -> str:
    content = html.escape(text).replace("\n", "<br>\n")
    return f"<p>{content}</p>"


@htmlize.register
def _(seq: abc.Sequence) -> str:
    inner = "</li>\n<li>".join(htmlize(item) for item in seq)
    return "<ul>\n<li>" + inner + "</li>\n</ul>"


@htmlize.register
def _(n: numbers.Integral) -> str:
    return f"<pre>{n} (0x{n:x})</pre>"


@htmlize.register
def _(n: bool) -> str:
    return f"<pre>{n}</pre>"


# Python 3.7之前可以用这种方式
@htmlize.register(fractions.Fraction)
def _(x) -> str:
    frac = fractions.Fraction(x)
    return f"<pre>{frac.numerator}/{frac.denominator}</pre>"


@htmlize.register(decimal.Decimal)
@htmlize.register(float)
def _(x) -> str:
    frac = fractions.Fraction(x).limit_denominator()
    return f"<pre>{x} ({frac.numerator}/{frac.denominator})</pre>"


print(htmlize({1, 2, 3}))
print(htmlize(abs))
print(htmlize("Heimlich & Co. \n- a game"))
print(htmlize(42))
print(htmlize(["alpha", 66, {3, 2, 2}]))
print(htmlize(True))
print(htmlize(2 / 3))
print(htmlize(fractions.Fraction(2, 3)))
print(htmlize(decimal.Decimal("0.232826")))
