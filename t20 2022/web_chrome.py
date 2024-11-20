from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set up the Selenium WebDriver
service = Service('C:/chromedriver-win64/chromedriver.exe')  # Adjust path accordingly
driver = webdriver.Chrome(service=service)

url = "https://www.espncricinfo.com/records/tournament/team-match-results/icc-men-s-t20-world-cup-2022-23-14450"
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Adjust this depending on your network speed

# Locate the table containing match data
table = driver.find_element(By.CLASS_NAME, 'ds-w-full')

# Extract all rows from the table
rows = []
for row in table.find_elements(By.TAG_NAME, 'tr')[1:]:  # Skip the header row
    cols = [col.text.strip() for col in row.find_elements(By.TAG_NAME, 'td')]
    rows.append(cols)

# Define the expected headers for the table
headers = ['Team 1', 'Team 2', 'Winner', 'Margin', 'Ground', 'Date', 'Match Number']

# Convert to DataFrame, filling missing columns with NaN
df = pd.DataFrame(rows, columns=headers)

if not df.empty:
    print(df.head())  # Print the first few rows to verify the DataFrame is populated
    
    # Save the DataFrame to CSV
    df.to_csv('icc_t20_worldcup_results_selenium.csv', index=False)
    print("Data saved to icc_t20_worldcup_results_selenium.csv")
else:
    print("No valid data to create DataFrame.")

# Extract match links from the 7th column (if available)
match_links = []
for row in table.find_elements(By.TAG_NAME, 'tr')[1:]:  # Skip the header row
    cols = row.find_elements(By.TAG_NAME, 'td')
    if len(cols) >= 7:  # Ensure at least 7 columns
        try:
            match_link = cols[6].find_element(By.TAG_NAME, 'a').get_attribute('href')
            match_links.append(match_link)
        except:
            continue

if match_links:
    print(f"Found {len(match_links)} match links: {match_links}")
else:
    print("No match links found.")

# Close the WebDriver
driver.quit()
