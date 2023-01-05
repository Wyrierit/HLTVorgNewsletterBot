import json
import requests
import time
from bs4 import BeautifulSoup

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
URL = "https://hltv.org"


def gethtmlandcontent():
    r = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    newsline_first = soup.find("div", class_="standard-box standard-list").find_all("a", class_="newsline article")
    urls = []
    news_dictionary = {}
    for news in newsline_first:
        news_url = URL + news.get("href")
        news_id = news_url.split("/")[-2]
        urls.append(news_url)
        for url in urls:
            noway = requests.get(url, headers=HEADERS).text
            soup2 = BeautifulSoup(noway, "html.parser")
            news_title = soup2.find("h1", class_="headline").text.strip()
            news_description = soup2.find("p", class_="headertext").text.strip()
            news_datetime = soup2.find("div", class_="date").text
            news_dictionary[news_id] = {
                "news_title": news_title,
                "news_url": news_url,
                "news_description": news_description,
                "news_datetime": news_datetime
            }
            time.sleep(1)
            # print(news_dict)
        with open("news_dictionary.json", "w", encoding="UTF-8") as file:
            json.dump(news_dictionary, file, indent=4, ensure_ascii=False)


def newnews():
    with open("news_dictionary.json", encoding="UTF-8") as file:
        news_dict = json.load(file)
    r = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    newsline_first = soup.find("div", class_="standard-box standard-list").find_all("a", class_="newsline article")
    urls = []
    fresh_dictionary = {}
    for news in newsline_first:
        news_url = URL + news.get("href")
        news_id = news_url.split("/")[-2]
        urls.append(news_url)
        if news_id in news_dict:
            continue
        else:
            for url in urls:
                noway = requests.get(url, headers=HEADERS).text
                soup2 = BeautifulSoup(noway, "html.parser")
                news_title = soup2.find("h1", class_="headline").text.strip()
                news_description = soup2.find("p", class_="headertext").text.strip()
                news_datetime = soup2.find("div", class_="date").text
                # news_first_image = soup2.find("img", class_="image").get("src")
                news_dict[news_id] = {
                    "news_title": news_title,
                    "news_url": news_url,
                    "news_description": news_description,
                    "news_datetime": news_datetime
                }
                fresh_dictionary[news_id] = {
                    "news_title": news_title,
                    "news_url": news_url,
                    "news_description": news_description,
                    "news_datetime": news_datetime
                }
                time.sleep(1)
    with open("news_dictionary.json", "w", encoding="UTF-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_dictionary


def main():
    # gethtmlandcontent()
    newnews()


if __name__ == "__main__":
    main()
