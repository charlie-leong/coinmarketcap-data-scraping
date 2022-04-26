from time import mktime
from datetime import date, timedelta
import requests
import csv


# data for 8:00:00 typically isn't available, this finds the lowest possible valid minute-second combination
def find_ms(json_data, key_date):
    for minutes in range(10):
        for seconds in range(60):
            ms = str("0" + str(minutes) + ":" + str(seconds))
            try:
                temp = json_data['data'][key_date + "T08:" + ms + ".999Z"]
                return ms
            except:
                ms = str("0" + str(minutes) + ":" + str(seconds))


today = date.today()
with open('global_cyptocurrency _chart.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["date", "market cap", "24h volume"])
    # trying to gather data from 90 days is often too much to handle
    # this splits it into thirds so it works consistently
    for third in range(3):
        start_date = today - timedelta(days=30 * third)
        end_date = start_date - timedelta(days=30)
        # print(start_date, end_date)

        start_date_timestamp = int(mktime(start_date.timetuple()))
        end_date_timestamp = int(mktime(end_date.timetuple()))

        url = ("https://web-api.coinmarketcap.com/v1.1/global-metrics/quotes/historical?format=chart&interval"
               "=5m&time_end=" + str(start_date_timestamp) + "&time_start=" + str(end_date_timestamp))
        response = requests.get(url)
        data = response.json()

        for day in range(1, 31):
            date = str(start_date - timedelta(days=day))
            minute_seconds = "04:11"
            try:
                key = date + "T08:" + minute_seconds + ".999Z"  # key format is str(yyyy-mm-ddThh:mm:ss.999Z)
                writer.writerow([date, data['data'][key][0], data['data'][key][1]])
            except Exception:
                minute_seconds = find_ms(data, date)
                key = date + "T08:" + str(minute_seconds) + ".999Z"
                writer.writerow([date, data['data'][key][0], data['data'][key][1]])

print("done")
