"""
Output membership function definitions for the fuzzy inference system.

These define the triangular membership functions for the output
variables (enhancement parameters) used during defuzzification.
"""

# Alpha (Contrast adjustment) - multiplier applied to pixel values
ALPHA = {
    "low": (0.8, 0.8, 1.0),
    "normal": (0.8, 1.0, 1.2),
    "high": (1.0, 1.2, 1.2)
}

# Beta (Brightness adjustment) - offset added to pixel values
BETA = {
    "low": (-20, -20, 0),
    "normal": (-20, 0, 20),
    "high": (0, 20, 20)
}

# Sharpen amount - kernel weight for sharpening filter
SHARPEN = {
    "low": (0, 0, 1),
    "medium": (0, 1, 2),
    "high": (1, 2, 2)
}

# Denoise amount - strength of noise reduction filter
DENOISE = {
    "low": (0, 0, 2),
    "medium": (0, 2, 5),
    "high": (2, 5, 5)
}