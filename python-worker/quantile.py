import pandas as pd

df = pd.read_csv("image_features.csv")
q1 = df["Sharpness"].quantile(0.25)
median = df["Sharpness"].quantile(0.50)
q3 = df["Sharpness"].quantile(0.75)

print("Q1:", q1)
print("Median:", median)
print("Q3:", q3)