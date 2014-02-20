#!/usr/bin/env python

# Import the required libraries
import argparse
from urllib2 import urlopen, URLError, HTTPError
from bs4 import BeautifulSoup

class Stock:

    def __init__(self, symbol):
        html = self.read_url(symbol)
        self.print_summary(symbol, html)
        self.print_call(symbol)
        #self.print_put(symbol)

    def read_url(self, symbol):
        url = 'http://finance.yahoo.com/q?s='+symbol
        try:
            response = urlopen(url)
        except HTTPError as e:
            print 'The server was unable to fulfill the request.'
            print 'Error code: ', e.code
        except URLError as e:
            print 'No network connection or the specified server does not exist.'
            print 'Reason: ', e.reason
        else:
            return response.read()

    def print_summary(self, symbol, html):
        print('summary')
        soup = BeautifulSoup(html)
        table = soup.find('table', id='table2')
        rows = table.findAll('tr')
        headers = list()
        datas = list()
        for row in rows:
            table_headers = row.findAll('th')
            table_data = row.findAll('td')
            for header in table_headers:
                headers.append(header.text)
            for data in table_data:
                datas.append(data.text)
        full = zip(headers, datas)
        for item in full:
            print "{0}{1}".format(item[0], item[1])

    def print_call(self, symbol):
        url = 'http://finance.yahoo.com/q/op?s='+symbol+'+Options'
        print url
        try:
            response = urlopen(url)
        except HTTPError as e:
            print 'The server was unable to fulfill the request.'
            print 'Error code: ', e.code
        except URLError as e:
            print 'No network connection or the specified server does not exist.'
            print 'Reason: ', e.reason
        else:
            soup = BeautifulSoup(response.read())
            table = soup.findAll("table", {"class" : "yfnc_datamodoutline1"})
            for t in table:
                rows = t.findAll('tr')
                for row in rows:
                    table_headers = row.findAll('th')
                    table_data = row.findAll('td')
                    for header in table_headers:
                        print (header.text)
                    for data in table_data:
                        print (data.text)

    def print_put(self, symbol):
        print('put')

def main():
    parser = argparse.ArgumentParser(description='Yahoo Finance Program')
    parser.add_argument('-s', '--stock', action='store',
        dest='stock', type=str, help='Stock Symbol used to gather information')
    args = parser.parse_args()

    if args.stock is None:
        parser.error("Must specify a stock symbol")

    stock = Stock(args.stock)

if __name__ == '__main__':
    main()

