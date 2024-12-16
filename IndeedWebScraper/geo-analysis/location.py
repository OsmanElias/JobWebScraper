from geopy.geocoders import Nominatim
import time
import pandas as pd
import os

# Initialize 
geolocator = Nominatim(user_agent="geo_analysis", timeout=10)


input_file = r'C:\Users\osman\OneDrive\Desktop\IndeedWebScraper\clean_data\combined_job_data.csv'
output_file = r'./geo-analysis/geocoded_jobs.csv'

# Read the data
data = pd.read_csv(input_file)

# for caching
if os.path.exists(output_file):
    geocoded_data = pd.read_csv(output_file)
    already_geocoded = set(geocoded_data['Location'])
else:
    geocoded_data = pd.DataFrame(columns=data.columns.tolist() + ['Latitude', 'Longitude'])
    already_geocoded = set()


def geocode_location(location):
    try:
        loc = geolocator.geocode(location)
        if loc:
            return loc.latitude, loc.longitude
        else:
            return None, None
    except Exception as e:
        return None, None

# Geocode each row
for index, row in data.iterrows():
    location = row['Location']
    if location in already_geocoded:
        continue  # Skip already processed 


    lat, lon = geocode_location(location)
    data.loc[index, 'Latitude'] = lat
    data.loc[index, 'Longitude'] = lon


    geocoded_data = pd.concat([geocoded_data, data.loc[[index]]], ignore_index=True)

    # Save progress every 10 rows
    if index % 10 == 0:
        geocoded_data.to_csv(output_file, index=False)
        print(f"Processed {index}/{len(data)} rows...")


geocoded_data.to_csv(output_file, index=False)
print(f"Geocoding completed. Saved to {output_file}.")