import pandas as pd

# Load
df = pd.read_csv("Social_Media_Advertising.csv")

# Fix data types
df['Acquisition_Cost'] = (df['Acquisition_Cost']
                          .str.replace('$', '', regex=False)
                          .str.replace(',', '', regex=False)
                          .astype(float))

df['Date'] = pd.to_datetime(df['Date'])

# Calculate CTR (missing from dataset — you must add this)
df['CTR'] = (df['Clicks'] / df['Impressions']) * 100

# Basic exploration
print("Shape:", df.shape)
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())
print("\nBasic Stats:\n", df.describe())

# Unique values in categorical columns
print("\nChannels:", df['Channel_Used'].unique())
print("Campaign Goals:", df['Campaign_Goal'].unique())
print("Customer Segments:", df['Customer_Segment'].unique())
print("Locations:", df['Location'].unique())

# Save clean version
df.to_csv("clean_dataset.csv", index=False)
print("\n✅ Clean dataset saved.")