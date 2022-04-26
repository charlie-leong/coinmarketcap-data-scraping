from time import mktime
from datetime import date, timedelta
import requests
import csv

ninety_days_ago = date.today() - timedelta(days=90)
today = date.today()

coins = []
coinNames = []
coinURL = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=60&sortBy=market_" \
          "cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=coins&tagType=all&audited=false&aux=ath,atl,high24h," \
          "low24h,num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply," \
          "volume_7d,volume_30d"
response = requests.get(coinURL)
topSixtyData = response.json()
for rank in range(60):
    coins.append(topSixtyData['data']['cryptoCurrencyList'][rank]['id'])
    coinNames.append(topSixtyData['data']['cryptoCurrencyList'][rank]['name'])

past_ninety_days_timestamp = int(mktime(ninety_days_ago.timetuple()))
today_timestamp = int(mktime(today.timetuple()))

print("Scraping from CoinMarketCap")

with open('inputData.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(['Name', 'Price', 'Market Cap', 'Volume', 'Change', 'Average Volume', 'Average Market Cap'])
    # for python 3.9.5
    # for (name, coin) in coins.items():
    # for python 3.5.6
    for coin in coins:
        url = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=' + str(
            coin) + '&convertId=2781&timeStart=' + str(past_ninety_days_timestamp) + '&timeEnd=' + str(today_timestamp)
        response = requests.get(url)
        data = response.json()
        today_quote_data = data['data']['quotes'][1]['quote']
        ninety_day_quote_data = data['data']['quotes'][0]['quote']

        days = len(data['data']['quotes'])  # should be 90 for most of them

        volumeTotal = 0
        marketCapTotal = 0
        for i in range(days):
            volumeTotal += data['data']['quotes'][i]['quote']['volume']
            marketCapTotal += data['data']['quotes'][i]['quote']['marketCap']

        averageVolume = volumeTotal / days
        averageMarketCap = marketCapTotal / days

        change_format = "{:.8f}"
        change = float(change_format.format(today_quote_data['close'])) / float(
            change_format.format(ninety_day_quote_data['close'])) - 1
        name = data['data']['name']
        writer.writerow(
            [name, today_quote_data['close'], today_quote_data['marketCap'], today_quote_data['volume'], change,
             averageVolume, averageMarketCap])

        print(name + " Success")
