"""
Utility functions for the ID-Oto Python worker.
"""

import os
import csv


def save_features_to_csv(features, filename="image_features.csv"):
    """
    Append image features to a CSV file for statistical analysis.

    Args:
        features (dict): Image features with keys:
            brightness, contrast, sharpness, noise
        filename (str): Path to the CSV file.
    """
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Brightness",
                "Contrast",
                "Sharpness",
                "Noise"
            ])

        writer.writerow([
            features["brightness"],
            features["contrast"],
            features["sharpness"],
            features["noise"]
        ])