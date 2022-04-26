import requests
from bs4 import BeautifulSoup
import csv
import json
import schedule
import time
from datetime import date


def get_top_spot_exchanges():
    url = "https://coinmarketcap.com/rankings/exchanges/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    with open('daily_top_spot_exchanges.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        data = json.loads(soup.find('script', attrs={'id': "__NEXT_DATA__"}).text)
        currency_names = [date.today()]
        currency_spotvol = [""]
        for currencies in range(90):
            currency_names.append(data['props']['initialProps']['pageProps']['exchange'][currencies]['name'])
            currency_spotvol.append(data['props']['initialProps']['pageProps']['exchange'][currencies]['spotVol24h'])

        writer.writerow(currency_names)
        writer.writerow(currency_spotvol)


schedule.every().day.at("08:00").do(get_top_spot_exchanges)

with open('daily_top_spot_exchanges.csv', 'w', newline='') as file:
    new_file = csv.writer(file)
    new_file.writerow(['date', 'name of currency'])
    new_file.writerow(['', 'spot volume over 24 hours'])

while True:
    schedule.run_pending()
    time.sleep(60)

