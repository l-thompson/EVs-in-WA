import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point
import us
import numpy as np

# Load the dataset
data_path = "Electric_Vehicle_Population_Data.csv"
ev_data = pd.read_csv(data_path)

# Data inspection and cleaning
print("Dataset Overview:")
print(ev_data.head())
print("\nColumns:", ev_data.columns)
print("\nBasic Info:")
ev_data.info()

# Extract latitude and longitude from 'Vehicle Location'
ev_data[['Longitude', 'Latitude']] = ev_data['Vehicle Location'].str.extract(r'POINT \(([^ ]+) ([^\)]+)\)')
ev_data['Latitude'] = pd.to_numeric(ev_data['Latitude'], errors='coerce')
ev_data['Longitude'] = pd.to_numeric(ev_data['Longitude'], errors='coerce')
ev_data.dropna(subset=['County', 'City', 'Vehicle Location', 'Latitude', 'Longitude'], inplace=True)

# Convert to GeoDataFrame for geospatial analysis
gdf = gpd.GeoDataFrame(
    ev_data,
    geometry=gpd.points_from_xy(ev_data.Longitude, ev_data.Latitude),
    crs="EPSG:4326"
)

# Exploratory Data Analysis (EDA)
# EV Type Distribution
plt.figure(figsize=(8, 6))
ev_type_counts = ev_data['Electric Vehicle Type'].value_counts()
ev_type_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Distribution of EV Types', fontsize=16)
plt.xlabel('Electric Vehicle Type', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('ev_type_distribution.png')
plt.show()

# EV Adoption by Model Year
plt.figure(figsize=(10, 6))
ev_data['Model Year'].value_counts().sort_index().plot(kind='bar', color='lightgreen', edgecolor='black')
plt.title('EV Registrations by Model Year', fontsize=16)
plt.xlabel('Model Year', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.tight_layout()
plt.savefig('ev_model_year.png')
plt.show()

# Top 10 EV Makes
plt.figure(figsize=(10, 6))
ev_make_counts = ev_data['Make'].value_counts().head(10)
sns.barplot(x=ev_make_counts.values, y=ev_make_counts.index, hue=ev_make_counts.index, palette='viridis', legend=False)
plt.title('Top 10 EV Makes by Registration Count', fontsize=16)
plt.xlabel('Number of Registrations', fontsize=12)
plt.ylabel('Make', fontsize=12)
plt.tight_layout()
plt.savefig('ev_make_counts.png')
plt.show()

# Electric Range Distribution
plt.figure(figsize=(10, 6))
sns.histplot(ev_data['Electric Range'], bins=30, kde=True, color='orange', edgecolor='black')
plt.title('Distribution of Electric Range', fontsize=16)
plt.xlabel('Electric Range (miles)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.tight_layout()
plt.savefig('electric_range.png')
plt.show()

# Visualizing Distribution of EVs by County
county_counts = ev_data['County'].value_counts().reset_index()
county_counts.columns = ['County', 'Count']

plt.figure(figsize=(10, 6))
sns.barplot(data=county_counts.head(10), x='Count', y='County', hue='County', palette='viridis', legend=False)
plt.title('Top 10 Counties by EV Registrations', fontsize=16)
plt.xlabel('Number of EVs', fontsize=12)
plt.ylabel('County', fontsize=12)
plt.tight_layout()
plt.savefig('county_counts.png')
plt.show()

# Mapping EV Registrations
# Load local TIGER shapefile
shp_path = "C:/Users/thomp/Documents/Website/EVs/shapefiles/tl_2021_us_county.shp"  # Adjust path if needed
counties_gdf = gpd.read_file(shp_path)

# Filter for Washington State counties
state_fips = us.states.lookup("Washington").fips
wa_counties = counties_gdf[counties_gdf['STATEFP'] == state_fips]

# Join EV registrations with counties
gdf = gdf.set_crs("EPSG:4326")
wa_counties = wa_counties.to_crs("EPSG:4326")
gdf_with_county = gpd.sjoin(gdf, wa_counties, how="inner", predicate="intersects")

# Count EVs per county based on join
gdf_county_counts = gdf_with_county['NAME'].value_counts().reset_index()
gdf_county_counts.columns = ['County', 'Count']

# Join spatial counts back to county GeoDataFrame
wa_counties = wa_counties.merge(gdf_county_counts, left_on='NAME', right_on='County', how='left')
wa_counties['Count'] = wa_counties['Count'].fillna(0)  # Fill missing counts with 0

# Apply logarithmic transformation for better color scaling (add 1 to avoid log(0))
wa_counties['Log_Count'] = np.log1p(wa_counties['Count'])

# Plot the map with logarithmic scale and annotations
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
wa_counties.plot(column='Log_Count', ax=ax, cmap='viridis', legend=True,
                 legend_kwds={'label': "Log(Number of EVs + 1)", 'shrink': 0.8})
plt.title('Distribution of EV Registrations Across Washington State', fontsize=16)
plt.axis('off')

# Annotate top 5 counties with their names and EV counts
top_counties = wa_counties.nlargest(5, 'Count')
for idx, row in top_counties.iterrows():
    centroid = row.geometry.centroid
    ax.annotate(f"{row['NAME']} ({int(row['Count'])})",
                xy=(centroid.x, centroid.y), xytext=(3, 3),
                textcoords="offset points", fontsize=8, color='black',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

plt.tight_layout()
plt.savefig('ev_map.png')
plt.show()