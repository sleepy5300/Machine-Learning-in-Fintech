import requests
import json
import csv
import time

# User input
year_start = 2017  # start year  
month_start = 1    # start month
year_end = 2018    # end year
month_end = 12     # end month
Stock_or_index = 1 # 下載台灣加權指數選 1，個股選 0
Stock_code = 2330  # Stock code
save_path = 'C:/Users/100505/Documents/Python Scripts/'  # Save Path

## Main Coding

# date creation
if Stock_or_index == 1:
    URL = 'http://www.twse.com.tw/indicesReport/MI_5MINS_HIST?response=json&date='   #證交所台灣加權指數網址，不含日期
    Stock_code = 'TWSE_Price'
else:
    URL = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='      #證交所個股網址，不含日期

year_list = range(year_start, year_end + 1)
month_list = range(1, 13)
month_list_start = range(month_start, 13)
month_list_end = range(1, month_end + 1)
month_list_range = range(month_start, month_end + 1)

date=[]
for year in year_list:
    if year_start == year_end:
        for month in month_list_range:
            date.append(str(year) + "{0:0=2d}".format(month) + '01')
    else:
        if year == year_start:
            for month in month_list_start:
                date.append(str(year) + "{0:0=2d}".format(month) + '01')
        elif year == year_end:
             for month in month_list_end:
                date.append(str(year) + "{0:0=2d}".format(month) + '01')
        else:
            for month in month_list:
                date.append(str(year) + "{0:0=2d}".format(month) + '01')

# Create new csv file for data output
save_path = save_path + '\\' + str(Stock_code) +'.csv'
outputfile = open(save_path, 'w', newline='', encoding='utf-8')
outputwriter = csv.writer(outputfile)

# Writing data to csv file
for dt in date:
    if Stock_or_index == 1:
        URL_dt = URL + dt
    else:
        URL_dt = URL + dt + '&stockNo='+ str(Stock_code)
      
    res = requests.get(URL_dt)
    time.sleep(2)
    s = json.loads(res.text)
  
    if dt == (str(year_start) + "{0:0=2d}".format(month_start) + '01'):
        outputwriter.writerow(s['fields'])
        for i in (s['data']):
            outputwriter.writerow(i)
    else:
        for i in (s['data']):
            outputwriter.writerow(i)

# Closing the csv file
outputfile.close()