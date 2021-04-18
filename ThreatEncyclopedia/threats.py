import pandas as pd

# script for data cleanup and export to csv

df = pd.read_json("threats.json")

df.to_csv("threats.csv", index=False)