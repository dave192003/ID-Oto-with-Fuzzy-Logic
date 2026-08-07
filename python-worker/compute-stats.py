import pandas as pd

filename = "image_features.csv"

def compute_statistics(filename):
    df = pd.read_csv(filename)

    stats = {
        "brightness": {
            "min": df["Brightness"].min(),
            "max": df["Brightness"].max(),
            "mean": round(df["Brightness"].mean(), 2),
            "std": round(df["Brightness"].std(), 2),
        },
        "contrast": {
            "min": df["Contrast"].min(),
            "max": df["Contrast"].max(),
            "mean": round(df["Contrast"].mean(), 2),
            "std": round(df["Contrast"].std(), 2),
        },
        "sharpness": {
            "min": df["Sharpness"].min(),
            "max": df["Sharpness"].max(),
            "mean": round(df["Sharpness"].mean(), 2),
            "std": round(df["Sharpness"].std(), 2),
        },
        "noise": {
            "min": df["Noise"].min(),
            "max": df["Noise"].max(),
            "mean": round(df["Noise"].mean(), 2),
            "std": round(df["Noise"].std(), 2),
        }
    }

    return stats

stats = compute_statistics(filename)
print(stats)