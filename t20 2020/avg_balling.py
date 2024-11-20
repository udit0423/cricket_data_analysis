import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.espncricinfo.com/records/season/averages-bowling/2021to22-2021to22/twenty20-internationals-3?trophy=89"
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

# Add an additional column header for the links
headers.insert(1, "Bowler Link")
print("Headers:", headers)

# Extract the rows
rows = []
for row in table.find_all('tr')[1:]:  # Skipping the header row
    cols = row.find_all('td')
    
    # Extract bowler name and link from the first column
    bowler_col = cols[0]
    bowler_name = bowler_col.text.strip()
    bowler_link = bowler_col.find('a')['href'] if bowler_col.find('a') else ''
    
    # Construct the full URL for the bowler link
    full_link = f"https://www.espncricinfo.com{bowler_link}" if bowler_link else ''
    
    # Extract the rest of the columns
    other_cols = [col.text.strip() for col in cols[1:]]
    
    # Prepend bowler name and link to the row
    row_data = [bowler_name, full_link] + other_cols
    
    if len(row_data) == len(headers):  # Only add rows with matching number of columns
        rows.append(row_data)
    else:
        print(f"Skipping row due to column mismatch: {row_data}")

# Convert to DataFrame for easy viewing
if headers and rows:
    df = pd.DataFrame(rows, columns=headers)
    print(df)
else:
    print("No valid data to create DataFrame.")

# Save the DataFrame to CSV
df.to_csv('avg_bowling_with_links.csv', index=False)
print("Data saved to avg_bowling_with_links.csv")