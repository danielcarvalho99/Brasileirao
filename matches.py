import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from rankings import URL, get_championship_links, filter_links, BEGINNING, END


def get_new_links(links):
    new_links = []

    for link in links:
        response = requests.get(link)

        current_url = response.url
        new_links.append(current_url)
    return new_links


def replace_new_links(links):
    new_links = []
    for link in links:
        new_link = link.replace('phases', 'games')
        new_links.append(new_link)
    return new_links


def page_exists(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.find_all('div')
    if len(divs) > 1:
        return 1
    return 0


def get_matches_links(links):
    matches_links = []
    for link in links:
        print(link)
        matches_page = 1
        curr_link = link + f'/p/{matches_page}'
        response = requests.get(curr_link)

        while page_exists(response):
            matches_links.append(curr_link)
            matches_page += 1
            curr_link = link + f'/p/{matches_page}'
            response = requests.get(curr_link)

    return matches_links


def get_year(link):
    pattern = re.compile(r'brasileiro-(\d+)')
    match = pattern.search(link)
    return match.group(1)


def get_matches(links):
    results = []
    for link in links:
        response = requests.get(link)
        year = get_year(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            classes = ['home_name', 'table_cell home_score', 'table_cell away_score', 'table_cell away_team']

            rows = soup.find_all('div', class_='table_row')
            for row in rows:
                result = []
                for curr_class in classes:
                    result.append(row.find(class_=curr_class).text.strip())
                result.append(year)
                results.append(result)

    return results


def generate_matches_df(matches):
    columns = ['Time_1', 'Gols_1', 'Gols_2', 'Time_2', 'Ano']
    df = pd.DataFrame(matches, columns=columns)

    columns.remove('Time_1')
    columns.remove('Time_2')
    df[columns] = df[columns].astype(int)

    return df


def matches_pipeline(url):
    links = get_championship_links(url)
    filtered_links = filter_links(links, BEGINNING, END)
    new_links = get_new_links(filtered_links)
    replaced_links = replace_new_links(new_links)

    matches_links = get_matches_links(replaced_links[:2])
    matches = get_matches(matches_links)
    df = generate_matches_df(matches)

    csv_file_path = 'matches_aux.csv'
    df.to_csv(csv_file_path, index=False)


matches_pipeline(URL)
