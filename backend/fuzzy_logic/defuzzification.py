import numpy as np

def centroid_defuzzify(output_set, membership_ranges, samples=1000):
   
    all_points = []
    for term, (a, b, c) in membership_ranges.items():
        all_points.extend([a, b, c])
    x_min, x_max = min(all_points), max(all_points)

    # Sample the universe of discourse
    x = np.linspace(x_min, x_max, samples)

    # Compute the aggregated membership at each sample point
    aggregated = np.zeros_like(x)
    for term, activation in output_set.items():
        if activation <= 0:
            continue
        a, b, c = membership_ranges[term]
        membership_curve = _triangular_curve(x, a, b, c)


        # Clip the membership curve to the activation level (min aggregation)
        aggregated = np.maximum(aggregated, np.minimum(membership_curve, activation))

    # Centroid calculation: sum(x * mu) / sum(mu)
    numerator = np.sum(x * aggregated)
    denominator = np.sum(aggregated)

    if denominator == 0:
        # return the midpoint of the universe
        return round(float((x_min + x_max) / 2), 4)

    return round(float(numerator / denominator), 4)


def _triangular_curve(x, a, b, c):

    x = np.asarray(x, dtype=float)
    result = np.zeros_like(x)

    if a == b:  # Left shoulder
        result[x <= b] = 1.0
        mask = (x > b) & (x < c)
        result[mask] = (c - x[mask]) / (c - b)
    elif b == c:  # Right shoulder
        result[x >= b] = 1.0
        mask = (x > a) & (x < b)
        result[mask] = (x[mask] - a) / (b - a)
    else:  # Normal triangle
        mask_left = (x > a) & (x < b)
        mask_right = (x >= b) & (x < c)
        result[x == b] = 1.0
        result[mask_left] = (x[mask_left] - a) / (b - a)
        result[mask_right] = (c - x[mask_right]) / (c - b)

    return result