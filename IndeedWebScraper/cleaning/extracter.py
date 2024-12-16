import pandas as pd
import os


file_data_analyst = './clean_data/data_analyst_cleaned.csv'
file_it_analyst = './scraped_data/extracted_jobs_IT_Analyst.csv'
file_software_developer = './scraped_data/extracted_jobs_Software_Developer.csv'
output_file = './clean_data/combined_job_data.csv'


data_analyst = pd.read_csv(file_data_analyst)
it_analyst = pd.read_csv(file_it_analyst)
software_developer = pd.read_csv(file_software_developer)

# Add a new column 
data_analyst['Job Type'] = 'Data Analyst'
it_analyst['Job Type'] = 'IT Analyst'
software_developer['Job Type'] = 'Software Developer'


data_analyst.rename(columns={'Cleaned Location': 'Location'}, inplace=True)
it_analyst.rename(columns={'Location': 'Location'}, inplace=True)
software_developer.rename(columns={'Location': 'Location'}, inplace=True)

# Combine 
combined_data = pd.concat([data_analyst[['Job Title', 'Location', 'Job Type']],
                            it_analyst[['Job Title', 'Location', 'Job Type']],
                            software_developer[['Job Title', 'Location', 'Job Type']]],
                           ignore_index=True)


combined_data.to_csv(output_file, index=False)
print(f"Combined dataset saved to {output_file}")

# Preview
print(combined_data.head())
