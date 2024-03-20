import re
from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = 'https://www.golaberto.com.br/championship/list?category=1&name=brasileiro&page=2&region=&utf8=%E2%9C%93'
BEGINNING = 2003
END = 2023


def get_championship_links(url):
    response = requests.get(url)
    championship_links = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', class_='championship_name')

        for div in divs:
            anchor_tags = div.find_all('a', href=True)

            for anchor in anchor_tags:
                championship_links.append(f"https://www.golaberto.com.br/{anchor['href']}")

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    return championship_links


def preprocess_year_and_championship(link):
    might_be_year = link.split(sep='-')[-2]

    if len(might_be_year) == 4:
        year = might_be_year
        championship = link.split(sep='-')[-3]
    else:
        year = link.split(sep='-')[-1]
        championship = link.split(sep='-')[-2]

    return int(year), championship


def filter_links(links, beginning, end):
    links = links[::3]
    new_links = []

    for link in links:
        year, championship = preprocess_year_and_championship(link)
        if (year <= end) and (year >= beginning) and championship != 'b':
            new_links.append(link)

    return new_links


def get_championship_records(links):
    records = []
    for link in links:
        year,_ = preprocess_year_and_championship(link)
        response = requests.get(link)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            table = tables[1]

            table_lines = table.find_all('tr', class_='table_line')

            for line in table_lines:
                curr_team = [year]
                cells = line.find_all('td')

                for cell in cells:
                    curr_team.append(cell.text.strip())

                curr_team[2] = curr_team[2][7:]

                records.append(curr_team)
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    return records


def generate_records_df(records):

    columns = ['Ano', 'Posição', 'Time', 'Pts', 'J', 'V', 'E', 'D', 'GF', 'GC', 'SG']
    df = pd.DataFrame(records, columns=columns)

    columns.remove('Time')
    df[columns] = df[columns].astype(int)

    return df


def rankings_pipeline(url):
    links = get_championship_links(url)
    links = filter_links(links, BEGINNING, END)
    records = get_championship_records(links)

    df = generate_records_df(records)
    csv_file_path = 'rankings.csv'
    df.to_csv(csv_file_path, index=False)


rankings_pipeline(URL)
