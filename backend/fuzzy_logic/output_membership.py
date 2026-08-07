
ALPHA = {
    "low": (0.7, 0.8, 1.0),
    "normal": (0.8, 1.0, 1.2),
    "high": (1.0, 1.2, 1.3)
}


# beta (Brightness adjustment)
# Negative = darker, Positive = brighter

BETA = {
    "low": (-30, -20, 0),
    "normal": (-20, 0, 20),
    "high": (0, 20, 30)
}


# Sharpen amount
# 0 = no sharpening, higher values = stronger sharpening

SHARPEN = {
    "low": (0, 0, 0.3),
    "medium": (0.2, 0.5, 0.8),
    "high": (0.7, 1.0, 1.2)
}

# Denoise strength
# Higher values remove more noise

DENOISE = {
    "low": (0, 0, 1.5),
    "medium": (1, 2.5, 4),
    "high": (3, 5, 6)
}