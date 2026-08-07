def triangular(x, a, b, c):

    if a == b:          # Left shoulder
        if x <= b:
            return 1.0
        elif x >= c:
            return 0.0
        return (c - x) / (c - b)

    if b == c:          # Right shoulder
        if x <= a:
            return 0.0
        elif x >= b:
            return 1.0
        return (x - a) / (b - a)

    # Normal triangle
    if x <= a or x >= c:
        return 0.0
    elif x == b:
        return 1.0
    elif x < b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)


def fuzzify(value, ranges):

    return {
        "low": triangular(value, *ranges["low"]),
        "medium": triangular(value, *ranges["medium"]),
        "high": triangular(value, *ranges["high"]),
    }