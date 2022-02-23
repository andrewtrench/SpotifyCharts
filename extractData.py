# Extract data from the downloaded files, save to a pandas dataframe

import bs4
import os
import pandas as pd



def chart_scraper(source_file):
    """Function to extract data from the files we saved earlier"""
    with open(f"sources/{source_file}", "r") as input_file:
        data = input_file.read()
    # Turn the content into soup
    soup = bs4.BeautifulSoup(data, features="html.parser")

    # Find all the rows in the html
    rows = soup.findAll('tr')

    week_df = pd.DataFrame(columns=['week_start', 'week_end', 'spotify_url', 'song', 'artist', 'streams'])


    # Iterate through each row and identify pieces of data based on the tags. Note we start at index [1] here as the
    # first row is a link to an explanation link which we don't need

    for row in rows[1:]:
        row_data = {'spotify_url': row.find('a', href=True)['href']}

        week_start = source_file.split('txt')[0].split('--')[0]
        week_end = source_file.split('txt')[0].split('--')[0]
        row_data['week_start'] = week_start
        row_data['week_end'] = week_end

        row_data['song'] = row.find_all('strong')[0].text

        row_data['artist'] = row.find_all('span')[0].text.replace('by ', '')

        row_data['streams'] = int(row.find('td', attrs={'class': 'chart-table-streams'}).text.replace(',', ''))

        # Save the dictionary to the dataframe
        week_df = week_df.append(row_data, ignore_index=True)
    
    return week_df
    # Save everything to an excel file
    #df.to_excel("spotify_sa_charts.xlsx", engine="openpyxl")


source_files = os.listdir('sources')
# Create a dataframe to hold all the extracted data
spotify_sa_df = pd.DataFrame(columns=['week_start', 'week_end', 'spotify_url', 'song', 'artist', 'streams'])

for f in source_files:
    print(f)
    spotify_sa_df=spotify_sa_df.append(chart_scraper(f))
spotify_sa_df.to_excel('spotify_sa_chart.xlsx', engine="openpyxl")