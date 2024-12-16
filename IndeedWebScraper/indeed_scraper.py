import requests
from bs4 import BeautifulSoup
import csv
import os

# Scraper API payload
payload = {
    'api_key': 'Use your own API key',
    'url': 'https://www.indeed.com/jobs?q=Data+Analyst&l=United+States&from=searchOnHP%2Cwhatautocomplete&vjk=15265239d7cece89',
    'autoparse': 'true',
    'output_format': 'html',  
    'country_code': 'us',
    'device_type': 'desktop',
    'max_cost': '100'
}

#request
response = requests.get('https://api.scraperapi.com/', params=payload)



output_file = "extracted_jobs.csv"



if response.status_code == 200:
  

    with open("response_data.txt", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("Response saved to 'response_data.txt'")
    
   
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find job cards 
    job_cards = soup.find_all('div', class_='job_seen_beacon')  
    
  
    extracted_jobs = []
    for job_card in job_cards:
        job_title = job_card.find('h2', class_='jobTitle').get_text(strip=True) if job_card.find('h2', class_='jobTitle') else "N/A"
        location = job_card.find('div', class_='company_location').get_text(strip=True) if job_card.find('div', class_='company_location') else "N/A"
        extracted_jobs.append((job_title, location))
        print(f"Job Title: {job_title}\nLocation: {location}\n")
    

     
    file_exists = os.path.isfile(output_file)
    
     # Write or append to the CSV file
    with open(output_file, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
   
        if not file_exists:
            writer.writerow(["Job Title", "Location"])
 
        writer.writerows(extracted_jobs)
    print(f"Extracted data appended to '{output_file}'")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    print("Response text:", response.text)

