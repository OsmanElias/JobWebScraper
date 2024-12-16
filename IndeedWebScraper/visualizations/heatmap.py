import folium
from folium.plugins import HeatMap
import pandas as pd

# Load data
data = pd.read_csv('./geo-analysis/geocoded_jobs.csv')

# Drop rows with missing 
data = data.dropna(subset=['Latitude', 'Longitude'])


base_map = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=5)


heat_data = data[['Latitude', 'Longitude']].values.tolist()
HeatMap(heat_data, min_opacity=0.5, max_zoom=18, radius=25, blur=15).add_to(base_map)

#legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 200px; height: 120px; 
            background-color: white; z-index:9999; font-size:14px;
            border:2px solid grey; border-radius:5px; padding: 10px;">
    <b>Heatmap Intensity</b><br>
    <i style="background: rgba(255, 0, 0, 0.9); width: 20px; height: 20px; display: inline-block;"></i> High Density<br>
    <i style="background: rgba(255, 165, 0, 0.7); width: 20px; height: 20px; display: inline-block;"></i> Medium Density<br>
    <i style="background: rgba(0, 255, 0, 0.5); width: 20px; height: 20px; display: inline-block;"></i> Low Density<br>
</div>
'''
base_map.get_root().html.add_child(folium.Element(legend_html))

# Save
base_map.save('./visualizations/job_hotspots_map_with_legend.html')
print("Map with legend saved to './visualizations/job_hotspots_map_with_legend.html'.")