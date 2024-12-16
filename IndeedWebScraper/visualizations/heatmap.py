import pandas as pd
import folium
from folium.plugins import HeatMap

# Load data
data = pd.read_csv(r'C:\Users\osman\OneDrive\Desktop\JobWebScraper\IndeedWebScraper\geo-analysis\cleaned_geocoded_jobs.csv')


print("Column names and types:", data.columns)
data.columns = data.columns.map(str)  

print("Rows with NaN values:", data[data.isna().any(axis=1)])


for col in ['Location', 'Job Type', 'Job Title']:
    data[col] = data[col].apply(lambda x: str(x) if not pd.isna(x) else "Unknown")
    print(f"Column '{col}' unique types:", data[col].map(type).unique())


data = data.dropna(subset=['Latitude', 'Longitude'])
data = data[(data['Latitude'].apply(lambda x: isinstance(x, (int, float)))) &
            (data['Longitude'].apply(lambda x: isinstance(x, (int, float))))]

# Create 
base_map = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=5)


def add_heatmap_layer(data, job_type, color_gradient):
    job_data = data[data['Job Type'].str.lower() == job_type]
    if not job_data.empty:
        heat_data = job_data[['Latitude', 'Longitude']].values.tolist()
        HeatMap(heat_data, min_opacity=0.5, max_zoom=18, radius=25, blur=15, gradient=color_gradient).add_to(base_map)
        print(f"Added heatmap for {job_type.capitalize()}")
    else:
        print(f"No data found for {job_type.capitalize()}")

# Add layers
add_heatmap_layer(data, 'data analyst', {0.2: 'green', 0.5: 'yellow', 0.9: 'red'})
add_heatmap_layer(data, 'it analyst', {0.2: 'blue', 0.5: 'lightblue', 0.9: 'darkblue'})
add_heatmap_layer(data, 'software developer', {0.2: 'purple', 0.5: 'violet', 0.9: 'darkviolet'})

# Add legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 250px; height: 160px; 
            background-color: white; z-index:9999; font-size:14px;
            border:2px solid grey; border-radius:5px; padding: 10px;">
    <b>Job Type Heatmap Legend</b><br>
    <i style="background: green; width: 20px; height: 20px; display: inline-block;"></i> Data Analyst<br>
    <i style="background: blue; width: 20px; height: 20px; display: inline-block;"></i> IT Analyst<br>
    <i style="background: purple; width: 20px; height: 20px; display: inline-block;"></i> Software Developer<br>
</div>
'''
base_map.get_root().html.add_child(folium.Element(legend_html))

# Save 
output_file = r'C:\Users\osman\OneDrive\Desktop\JobWebScraper\IndeedWebScraper\visualizations\job_types_heatmap_with_legend.html'
base_map.save(output_file)
print(f"Map saved to {output_file}")
