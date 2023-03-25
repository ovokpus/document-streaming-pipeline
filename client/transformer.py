import numpy as np
from numpy import add
import pandas as pd


df = pd.read_csv("./data/data.csv")
print(df)

# add json column to the dataframe
# splitlines will split the json into multiple rows not a single one
df["json"] = df.to_json(orient="records", lines=True).splitlines()

# Take the json column of the dataframe
df_json = df["json"]
print(df_json)
print("transform completed!")

# escape timestamp forward slash with backslash
np.savetxt(r'./data/output.txt', df_json.values, fmt='%s')