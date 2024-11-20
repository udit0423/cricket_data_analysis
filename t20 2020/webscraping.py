import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.espncricinfo.com/records/season/team-match-results/2021to22-2021to22?trophy=89"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully fetched the page!")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')

# Find the table containing the match data
table = soup.find('table', {'class': 'ds-w-full'})

# Extract the headers
headers = [header.text for header in table.find_all('th')]
if not headers:  # Fallback if headers are missing
    headers = [col.text.strip() for col in table.find_all('tr')[0].find_all('td')]

print("Headers:", headers)

# Extract the rows
rows = []
for row in table.find_all('tr')[1:]:  # Skipping the header row
    cols = row.find_all('td')
    cols = [col.text.strip() for col in cols]
    if len(cols) == len(headers):  # Only add rows with matching number of columns
        rows.append(cols)
    else:
        print(f"Skipping row due to column mismatch: {cols}")

# Convert to DataFrame for easy viewing
if headers and rows:
    df = pd.DataFrame(rows, columns=headers)
    print(df)
else:
    print("No valid data to create DataFrame.")

# Save the DataFrame to CSV
df.to_csv('icc_t20_worldcup_results_fixed.csv', index=False)
print("Data saved to icc_t20_worldcup_results_fixed.csv")

import time

# Extract match links from the 7th column
match_links = []
for row in table.find_all('tr')[1:]:  # Skipping the header row
    cols = row.find_all('td')
    if cols and len(cols) >= 7:  # Ensure there are at least 7 columns
        match_link_tag = cols[6].find('a')  # Look for the anchor tag in the 7th column
        if match_link_tag:  # Ensure the anchor tag exists
            match_link = match_link_tag['href']
            match_links.append(match_link)

if not match_links:
    print("No match links found.")
else:
    print(f"Found {len(match_links)} match links.")

import time
import urllib3

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
# Function to scrape batting and bowling data from a match's scorecard
# Extract batting and bowling data from multiple sections
def scrape_match_data(match_url):
    try:
        response = requests.get(match_url)
        response.raise_for_status()
        match_soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all tables
        tables = match_soup.find_all('table', class_='ds-table')

        batting_data = []
        bowling_data = []

        # Iterate through the tables for both batting and bowling sections
        for index, table in enumerate(tables):
            rows = table.find_all('tr')
            if len(rows) > 1:
                # Check if it's a batting table (1st and 3rd tables)
                if index % 2 == 0:  # Batting tables at index 0 and 2
                    for row in rows[1:]:  # Skip the header row
                        cols = row.find_all('td')
                        if len(cols) >= 8:  # Ensure there are enough columns
                            batsman = {
                                'batsmanName': cols[0].text.strip(),
                                'runs': cols[2].text.strip(),
                                'balls': cols[3].text.strip(),
                                'minutes': cols[4].text.strip() if len(cols) > 4 else '',
                                '4s': cols[5].text.strip() if len(cols) > 5 else '',
                                '6s': cols[6].text.strip() if len(cols) > 6 else '',
                                'SR': cols[7].text.strip() if len(cols) > 7 else ''
                            }
                            batting_data.append(batsman)
                
                # Check if it's a bowling table (2nd and 4th tables)
                elif index % 2 == 1:  # Bowling tables at index 1 and 3
                    for row in rows[1:]:  # Skip the header row
                        cols = row.find_all('td')
                        if len(cols) >= 11:  # Ensure there are enough columns for bowling details
                            bowler = {
                                'bowlerName': cols[0].text.strip(),
                                'overs': cols[1].text.strip(),
                                'maidens': cols[2].text.strip(),
                                'runs': cols[3].text.strip(),
                                'wickets': cols[4].text.strip(),
                                'economy': cols[5].text.strip(),
                                'dots': cols[6].text.strip(),
                                'fours': cols[7].text.strip(),
                                'sixes': cols[8].text.strip(),
                                'wides': cols[9].text.strip(),
                                'no_balls': cols[10].text.strip()
                            }
                            bowling_data.append(bowler)

        return batting_data, bowling_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {match_url}: {e}")
        return [], []

# Base URL
base_url = "https://www.espncricinfo.com"

# List to store all match data
rows = []
for relative_url in match_links:
    match_url = f"{base_url}{relative_url}"  # Create absolute URL
    print(f"Scraping data from: {match_url}")

    # Scrape data for this match
    batting_data, bowling_data = scrape_match_data(match_url)

    # Add match_id for the dataset
    match_id = relative_url.split('/')[-1].split('-')[-1]
    for batsman in batting_data:
        batsman['match_id'] = match_id
    for bowler in bowling_data:
        bowler['match_id'] = match_id

    # Append the results
    rows.append((batting_data, bowling_data))

    # Delay to avoid overwhelming the server (good practice)
    time.sleep(2)

# Convert scraped data to DataFrames and save to CSV
batting_df = pd.DataFrame([batsman for match in rows for batsman in match[0]])
bowling_df = pd.DataFrame([bowler for match in rows for bowler in match[1]])

# Save batting data to CSV
if not batting_df.empty:
    batting_df.to_csv('icc_t20_worldcup_batting.csv', index=False)
    print("Batting data saved to icc_t20_worldcup_batting.csv")
else:
    print("No batting data found!")

# Save bowling data to CSV
if not bowling_df.empty:
    bowling_df.to_csv('icc_t20_worldcup_bowling.csv', index=False)
    print("Bowling data saved to icc_t20_worldcup_bowling.csv")
else:
    print("No bowling data found!")

