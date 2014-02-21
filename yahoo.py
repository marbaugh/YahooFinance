#!/usr/bin/env python

# Import the required libraries
import argparse

from urllib2 import urlopen, URLError, HTTPError
from bs4 import BeautifulSoup

class StockInfo:
    """Stock Info Class creates an instance of StockInfo
    
    Provides an init method to set the urls necessary to provide stock info

    and other methods to get the stocks summary info, call info, and put info
    
    """

    def __init__(self, symbol):
        """Init method creates the objects summary and options urls"""

        self.summary_url = 'http://finance.yahoo.com/q?s='+symbol
        self.options_url = 'http://finance.yahoo.com/q/op?s='+symbol+'+Options'

        
    def _get_url(self, url):
        """Private class method to read and return a given url"""
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

    def summary_info(self):
        """Summary_info method parses the summary html from the summary_url"""

        soup = BeautifulSoup(self._get_url(self.summary_url))
        headers = list() #list to hold talbe headers
        values = list() #list to told table values
        ids = ['table1', 'table2']

        for table_id in ids:
            table = soup.find('table', id=table_id)
            rows = table.findAll('tr')
            for row in rows:
                table_headers = row.findAll('th')

                table_data = row.findAll('td')
                for header in table_headers:
                    headers.append(header.text)
                for data in table_data:
                    values.append(data.text)

        return zip(headers, values)
    
def main():
    parser = argparse.ArgumentParser(description='Yahoo Finance Program')
    parser.add_argument('-s', '--stock', action='store',

        dest='stock', type=str, help='Stock Symbol used to gather information')
    args = parser.parse_args()

    if args.stock is None:
        parser.error("Must specify a stock symbol")


    stock = StockInfo(args.stock)
    summary = stock.summary_info()
    for item in summary:
        print "{0}{1}".format(item[0], item[1])

if __name__ == '__main__':
    main()
