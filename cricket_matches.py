import csv

# Data to be written to the CSV file
data = [
    ["match", "year", "links"],
    ["t20", "2020", "https://www.espncricinfo.com/records/season/team-match-results/2021to22-2021to22?trophy=89"],
    ["t20", "2022", "https://www.espncricinfo.com/records/season/team-match-results/2022to23-2022to23?trophy=89"],
    ["t20", "2024", "https://www.espncricinfo.com/records/tournament/team-match-results/icc-men-s-t20-world-cup-2024-15946"],
    ["ipl", "2024", "https://www.espncricinfo.com/records/season/team-match-results/2024-2024?trophy=117"],
    ["ipl", "2023", "https://www.espncricinfo.com/records/season/team-match-results/2023-2023?trophy=117"],
    ["ipl", "2022", "https://www.espncricinfo.com/records/season/team-match-results/2022-2022?trophy=117"],
    ["ipl", "2021", "https://www.espncricinfo.com/records/season/team-match-results/2021-2021?trophy=117"],
    ["ipl", "2020", "https://www.espncricinfo.com/records/season/team-match-results/2020to21-2020to21?trophy=117"],
    ["odi", "2024", "https://www.espncricinfo.com/records/season/team-match-results/2023to24-2023to24?trophy=12"],
    ["odi", "2019", "https://www.espncricinfo.com/records/season/team-match-results/2019-2019?trophy=12"],
]

# Specify the CSV file name
csv_file = "cricket_matches.csv"

# Writing to the CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"CSV file '{csv_file}' created successfully.")
