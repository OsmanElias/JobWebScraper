import pandas as pd
import re
import os


input_file = './scraped_data/extracted_jobs_Software_Developer.csv'  
output_directory = './clean_data/'  
output_file = os.path.join(output_directory, 'software_developer_cleaned.csv') 



os.makedirs(output_directory, exist_ok=True)

# Read the CSV
data = pd.read_csv(input_file)


print("Columns in the dataset:", data.columns)


required_columns = ['Job Title', 'Company Name', 'Location']
missing_columns = [col for col in required_columns if col not in data.columns]


if missing_columns:
    print(f"Error: Missing required columns: {missing_columns}")
else:

    def clean_column(value):
        if pd.isna(value):
            return None
        return value.strip()

    data['Job Title'] = data['Job Title'].apply(clean_column)
    data['Company Name'] = data['Company Name'].apply(clean_column)
    data['Location'] = data['Location'].apply(clean_column)

   
    def clean_company_name(company):
        if company:
            return re.sub(r'\d+\.\d+', '', company).strip()
        return company

    data['Company Name'] = data['Company Name'].apply(clean_company_name)


    def split_company_location(value):
        if pd.isna(value):
            return pd.Series([None, None])
      
        match = re.search(r'^(.*?)([A-Za-z]+\s*[A-Za-z]*)?\s*(?:,|\sin\s|\sat\s)(.*)$', value)
        if match:
            company = match.group(1).strip()
            location = match.group(3).strip() if match.group(3) else None
            return pd.Series([company, location])
        return pd.Series([value.strip(), None])

   
    split_columns = data['Company Name'].apply(split_company_location)
    data['Cleaned Company Name'] = split_columns[0]
    data['Cleaned Location'] = split_columns[1]


    print("Sample data after splitting:")
    print(data[['Job Title', 'Cleaned Company Name', 'Cleaned Location']].head())

   
    data.drop(columns=['Company Name', 'Location'], inplace=True)


    data.to_csv(output_file, index=False)
    print(f"Cleaned and separated data saved to {output_file}")










