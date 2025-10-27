"""Utility functions for demonstrating CI stages."""

from __future__ import annotations

"""Ejercicio de importacion futura"""

def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b


def safe_divide(a: float, b: float) -> float:
    """Return the quotient of two numbers, raising on zero divisor."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
