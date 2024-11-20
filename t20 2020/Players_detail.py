import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def extract_player_data(player_url, session):
    """
    Extract player data from the given URL.
    
    Args:
        player_url (str): The URL of the player.
        session (requests.Session): A requests session object.
        
    Returns:
        dict: A dictionary containing player data.
    """
    try:
        response = session.get(player_url)
        response.raise_for_status()  # Raise an error for bad responses
        player_soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the relevant div containing player details
        player_details = player_soup.find('div', class_='ds-grid lg:ds-grid-cols-3 ds-grid-cols-2 ds-gap-4 ds-mb-8')
        if not player_details:
            print(f"Player details not found for {player_url}")
            return {}

        # Extract individual data points from the div
        player_data = {}
        
        # Function to extract text from elements
        def extract_text(label):
            elem = player_details.find('p', text=label)
            if elem:
                return elem.find_next('span').text.strip()
            return None

        # Extract fields
        player_data['Full Name'] = extract_text('Full Name')
        player_data['Born'] = extract_text('Born')
        player_data['Age'] = extract_text('Age')
        player_data['Batting Style'] = extract_text('Batting Style')
        player_data['Bowling Style'] = extract_text('Bowling Style')
        player_data['Playing Role'] = extract_text('Playing Role')

        # Extract Country Name
        country_elem = player_soup.find('a', title=lambda x: x and "cricket team profile" in x)
        if country_elem:
            player_data['Country'] = country_elem.find('span', class_='ds-text-title-s').text.strip()
        
        return player_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {player_url}: {e}")
        return {}

def main():
    # Load player URLs from CSV
    df1 = pd.read_csv('avg_batting_with_links.csv')
    player_urls_batting = df1['Batsman Link'].tolist()
    
    # Initialize session
    with requests.Session() as session:
        all_players_data = []
        for player_url in player_urls_batting:
            print(f"Extracting data for {player_url}")
            player_data = extract_player_data(player_url, session)
            if player_data:
                all_players_data.append(player_data)
            # Sleep for a random time between requests to avoid being blocked
            time.sleep(random.uniform(1, 3))

        # Convert to DataFrame and save to CSV
        df = pd.DataFrame(all_players_data)
        csv_filename = 'players_data.csv'
        df.to_csv(csv_filename, index=False)
        print(f"Player data saved to {csv_filename}")

if __name__ == "__main__":
    main()
