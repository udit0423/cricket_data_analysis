import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def extract_player_data(player_url):
    try:
        response = requests.get(player_url)
        response.raise_for_status()
        player_soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the relevant div containing player details
        player_details = player_soup.find('div', class_='ds-grid lg:ds-grid-cols-3 ds-grid-cols-2 ds-gap-4 ds-mb-8')
        if not player_details:
            print(f"Player details not found for {player_url}")
            return {}

        # Extract individual data points from the div
        player_data = {}
        
        # Extract Full Name
        full_name_elem = player_details.find('p', text='Full Name')
        if full_name_elem:
            full_name = full_name_elem.find_next('span').text.strip()
            player_data['Full Name'] = full_name
        
        # Extract Born (Date of Birth)
        born_elem = player_details.find('p', text='Born')
        if born_elem:
            born = born_elem.find_next('span').text.strip()
            player_data['Born'] = born
        
        # Extract Age
        age_elem = player_details.find('p', text='Age')
        if age_elem:
            age = age_elem.find_next('span').text.strip()
            player_data['Age'] = age
        
        # Extract Batting Style
        batting_style_elem = player_details.find('p', text='Batting Style')
        if batting_style_elem:
            batting_style = batting_style_elem.find_next('span').text.strip()
            player_data['Batting Style'] = batting_style
        
        # Extract Bowling Style
        bowling_style_elem = player_details.find('p', text='Bowling Style')
        if bowling_style_elem:
            bowling_style = bowling_style_elem.find_next('span').text.strip()
            player_data['Bowling Style'] = bowling_style
        
        # Extract Playing Role
        playing_role_elem = player_details.find('p', text='Playing Role')
        if playing_role_elem:
            playing_role = playing_role_elem.find_next('span').text.strip()
            player_data['Playing Role'] = playing_role

        # Extract Country Name
        country_elem = player_soup.find('a', title=lambda x: x and "cricket team profile" in x)
        if country_elem:
            country_name = country_elem.find('span', class_='ds-text-title-s').text.strip()
            player_data['Country'] = country_name
        
        return player_data

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching data from {player_url}: {e}")
        return {}
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error fetching data from {player_url}: {e}")
        return {}
    except Exception as e:
        print(f"An error occurred fetching data from {player_url}: {e}")
        return {}

# List of player URLs
df1 = pd.read_csv('avg_batting_with_links.csv')
player_urls_batting = df1['Batsman Link'].tolist()
player_urls = player_urls_batting

# Print the combined list of player URLs
print("Combined player URLs:", player_urls)

# Extract data for all players
all_players_data = []
for player_url in player_urls:
    print(f"Extracting data for {player_url}")
    player_data = extract_player_data(player_url)
    if player_data:
        all_players_data.append(player_data)
    # Sleep to avoid overwhelming the server with requests
    time.sleep(1)  # Adjust the sleep time as necessary

# Convert to DataFrame and save to CSV
df = pd.DataFrame(all_players_data)

# Save the data to CSV file
csv_filename = 'players_data.csv'
df.to_csv(csv_filename, index=False)

print(f"Player data saved to {csv_filename}")
