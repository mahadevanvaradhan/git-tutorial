import os

def fibonacci_series(n):
    """Return a list containing the Fibonacci series up to n terms."""
    series = []
    a, b = 0, 1
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return series

# Example usage:
if __name__ == "__main__":
    terms = 10
    print(f"Fibonacci series up to {terms} terms: {fibonacci_series(terms)}")