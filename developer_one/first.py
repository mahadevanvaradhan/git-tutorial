import os

def fibonacci_series(n):
    """Return a list containing the Fibonacci series up to n terms."""
    series = []
    a, b = 0, 1
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return series

def area_of_circle(radius):
    """Return the area of a circle given its radius."""
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    if not isinstance(radius, (int, float)):
        raise TypeError("Radius must be a number")
    return 3.141592653589793 * radius * radius


# Example usage:
if __name__ == "__main__":
    terms = 10
    print(f"Fibonacci series up to {terms} terms: {fibonacci_series(terms)}")