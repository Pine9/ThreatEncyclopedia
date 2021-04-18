import pandas as pd
import numpy as np

# script for data cleanup and export to csv

df = pd.read_json("threats.json")

# fixing 'file size': ints, in units of bytes
# 'Unknown' and 'Varies' are non-numerical and won't be missed if they are simply replaced with NaN
df['file size'] = df['file size'].replace('Unknown', '0')
df['file size'] = df['file size'].apply(lambda x :
        int(x.replace('(Varies)', '0').replace('Varies', '0').replace('bytes', '').replace(',', '').replace(' ', '')))
df['file size'] = df['file size'].replace(0, np.NaN)

# fixing 'memory resident?': boolean, or None for unknown
df['memory resident?'] = df['memory resident?'].map({'Unknown': None, ' Yes': True, ' No': False})

df.to_csv("threats.csv", index=False)