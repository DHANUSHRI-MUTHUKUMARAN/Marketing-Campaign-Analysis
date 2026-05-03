import pandas as pd

df = pd.read_csv("Social_Media_Advertising.csv")  # adjust file name if needed

df.head()

df.info()
df.describe()
df.isnull().sum()
df['Channel_Used'].value_counts()