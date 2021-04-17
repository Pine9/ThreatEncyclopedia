import pandas as pd

df = pd.read_json("threats.json")
df.to_csv("threats.csv", index=False)