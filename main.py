import requests
import pandas as pd
import matplotlib.pyplot as plt

# Set API endpoint and parameters
url = "https://api.inaturalist.org/v1/observations"
params = {
    "taxon_id": 3,  # Bird taxon ID
    "per_page": 100, # Number of results per page
    "page": 1
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Convert observations to a pandas DataFrame
observations = data['results']
df = pd.DataFrame(observations)

# Display the data structure
print(df.head())

# Example: Extract useful columns like species name and location
df['species_name'] = df['taxon'].apply(lambda x: x['name'] if x else None)
df['latitude'] = df['geojson'].apply(lambda x: x['coordinates'][1] if x else None)
df['longitude'] = df['geojson'].apply(lambda x: x['coordinates'][0] if x else None)

# Filter out missing data
df_clean = df.dropna(subset=['species_name', 'latitude', 'longitude'])

print(df_clean[['species_name', 'latitude', 'longitude']].head())

# Plot species distribution with matplotlib
species_count = df_clean['species_name'].value_counts().head(10)
species_count.plot(kind='bar')
plt.title('Top 10 Most Observed Bird Species')
plt.ylabel('Number of Observations')
plt.show()

plt.scatter(x=df['longitude'], y=df['latitude'])
plt.show()