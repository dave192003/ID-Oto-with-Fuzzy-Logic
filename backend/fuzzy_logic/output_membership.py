# Alpha - contrast adjustment
ALPHA = {
    "low": (0.85, 0.85, 1.0),
    "normal": (0.9, 1.0, 1.1),
    "high": (1.0, 1.1, 1.15)
}


# Beta - brightness adjustment
# High brightness → Low beta → darker image
BETA = {
    "low": (-50, -50, 0),
    "normal": (-50, 0, 10),
    "high": (9, 11, 12)
}


# Sharpen amount - controlled
SHARPEN = {
    "low": (0.0, 0.0, 0.20),
    "medium": (0.15, 0.25, 0.35),
    "high": (0.30, 0.40, 0.50)
}


# Denoise amount - stronger
DENOISE = {
    "low": (0, 0, 2.0),
    "medium": (2.5, 3.2, 4.0),
    "high": (4.0, 5.0, 6.0)
}