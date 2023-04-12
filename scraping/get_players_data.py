import json

import requests
from bs4 import BeautifulSoup

# ホームから各チームの「選手一覧」のURLを取得する
url = "https://baseball-data.com/"
headers = {"User-Agent": "Mozilla/5.0"}  # リクエストヘッダーがないとbot判定され403が返される


def get_players_list_urls(url, headers):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find_all("table", attrs={"class": "stats-menu"})
    tables = table[:2]
    team_urls = []
    for table in tables:
        trs = table.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            team_url = tds[1].a.get("href")
            team_urls.append(team_url)
    return team_urls


# 選手一覧から各選手のURLを取得する
def get_player_urls(url, headers):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    trs = soup.tbody.find_all("tr")
    player_urls = []
    for tr in trs:
        tds = tr.find_all("td")
        player_url = tds[1].a.get("href")
        player_urls.append(player_url)
    return player_urls


# 各選手の個人データを取得する
def get_players_data(url, headers):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    uniform_number = soup.h2.text.split("(")[0].split(" ")[0]
    name = soup.h2.text.split("(")[0].split(" ")[1].replace("　", "")
    trs = soup.table.find_all("tr")
    all_data = []
    for tr in trs:
        tds = tr.find_all("td")
        for td in tds:
            all_data.append(td.text)
    born = all_data[0].replace("年", "/").replace("月", "/").replace("日", "")
    height = all_data[6].replace("cm", "")
    weight = all_data[8].replace("kg", "")
    salary = all_data[9].replace("万円（推定）", "").replace(",", "")
    team_name = url.split("/")[-2]

    player_data = {
        "name": name,
        "born": born,
        "height": height,
        "weight": weight,
        "salary": salary,
        "uniform_number": uniform_number,
        "team_name": team_name,
    }

    return player_data


def main():
    team_urls = get_players_list_urls(url, headers)

    all_players_urls = []
    for team_url in team_urls:
        team_player_urls = get_player_urls(team_url, headers)
        all_players_urls.append(team_player_urls)
    all_players_data = []
    for player_urls in all_players_urls:
        for player_url in player_urls:
            player_data = get_players_data(player_url, headers)
            all_players_data.append(player_data)
    with open("players_data.json", "w", encoding="utf-8") as f:
        # ensure_asciiでUnicodeエスケープを解除
        json.dump(all_players_data, f, indent=2, ensure_ascii=False)
        f.write(",\n")


if __name__ == "__main__":
    main()
