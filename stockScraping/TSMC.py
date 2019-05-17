from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import csv
import time
import pandas as pd
import matplotlib.pyplot as plt

# define global variables
# def initGB():
global SPATH
SPATH = r"./TSMC_test.csv"


# draw price trending
def draw_price():
    df = pd.read_csv(SPATH)
    # fetch the "end price" of each of the day
    END_PRICE = df['End']
    plt.plot(df['date'], END_PRICE)
    plt.show()

def main():
    month_list = [f'{(i+1):02d}' for i in range(3)]

    with open(SPATH, "a", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['date', 'Amounts', 'Price', 'O', 'H', 'L', 'End', '%'])
    
    for month in month_list:
        # get data from different date
        tsmc_web = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=2015'\
                    + month\
                    + '05&stockNo=2330'

###############################################
        # stock_code = str(input(
        #     'Plz enter the stock code that you want to search:\n'))
        # tsmc_web = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=2015'\
        #         + month\
        #         + '05&stockNo=2'\
        #         + stock_code
###############################################

        # get html
        res = urlopen(tsmc_web).read()
        # parser html
        soup = BeautifulSoup(res, 'lxml')
        # from "web inspect" find the tags you want 
        data_tag = 'tr td'
        # fetch the specific content
        articles = soup.select(data_tag)

        # write data
        with open(SPATH, "a", newline='') as csv_file:
            writer = csv.writer(csv_file)
            data_list = []
            for i, art in enumerate(articles):
                if (i+1) % 9 == 0 and (i+1) > 9:
                    print('write', data_list)
                    writer.writerow(data_list)
                    data_list = []
                else:
                    if (i+1) > 9:
                        print('save', art.text)
                        data_list.append(art.text)
        time.sleep(2)

if __name__ == "__main__":
    # try:
    main()
    # except:
    #     print("Please close the saving data!")
    # draw_price()
