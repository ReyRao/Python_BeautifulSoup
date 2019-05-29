from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import csv
import time
import pandas as pd
import matplotlib.pyplot as plt

class StockScraping():
    def __init__(
            self,
            stockCode='2330',
            year='2018',
            month='01'):
        self.stockCode = stockCode
        self.year = year
        self.month = month
        self.SPATH = f"./{self.stockCode}.csv"
        
    # draw price trending
    def drawTrend(self, para):
        self.para = para
        df = pd.read_csv(self.SPATH )
        x = list(range(len(df['date'])))
        # fetch the "end price" of each of the day
        plt.plot(df['date'], df[self.para])
        plt.xticks(x, df['date'], rotation='vertical')
        plt.show()

    # in which year and which stockCode you want
    def scrape(self):
        month_list = [f'{(i+1):02d}' for i in range(2)]
        for month in month_list:
            # get data from different date
            web = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date='\
                + self.year\
                + month\
                + '05&stockNo='\
                + self.stockCode
            # get html
            res = urlopen(web).read()
            # parse html
            soup = BeautifulSoup(res, 'lxml')
            # from "web inspect" find the tags you want
            data_tag = 'tr td'
            # fetch the specific content
            articles = soup.select(data_tag)

            # try to open the file
            try:
                with open(self.SPATH, "a", newline='') as csv_file:
                    pass
                    # print(f'Get the data {self.year}/{month} successfully!')
            except:
                print("Please close the saving data!")
                break

            # write data
            with open(self.SPATH, "a", newline='') as csv_file:
                writer = csv.writer(csv_file)
                data_list = []
                for i, art in enumerate(articles):
                    if (i+1) % 9 == 0 and (i+1) > 9:
                        # print('write', data_list)
                        writer.writerow(data_list)
                        data_list = []
                    else:
                        if (i+1) > 9:
                            data_list.append(art.text)
            time.sleep(2)


def main():
    taiwan50 = StockScraping(stockCode='0050', year='2018')
    print(f'Saving path: {taiwan50.SPATH}')

    fisrtOpen = str(input("Do you have the existed data?!(y/n)"))
    
    if fisrtOpen == "y" or fisrtOpen == "Y":
        fisrtOpen = True
    else:
        fisrtOpen = False

    if fisrtOpen == True:
        try:
            with open(taiwan50.SPATH, "a", newline='') as csv_file:
                writer = csv.writer(csv_file)
                print('write header')
                writer.writerow(['date', 'Amounts', 'Price', 'O', 'H', 'L', 'End', 'Diff'])
        except:
            print("Please close the saving data!")

    try:
        taiwan50.scrape()
        print(f'Get the data ({taiwan50.stockCode}, year:{taiwan50.year}) successfully!')
    except:
        print("Scrape wrong!")

    # taiwan50.drawTrend('O')


if __name__ == "__main__":
    main()
