'''
define a function
input: dataframe
country code, city, date
output: dict{date, temperature, humidity, condition}
'''
# import package
import pandas as pd
from datetime import datetime, timedelta
from time import sleep
import bs4
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import numpy as np
import csv
import argparse

# set parameters
parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input_file', help='input path', type=str)
parser.add_argument('--browser', dest='browsername', help='chromedriver path', default='./chromedriver')
parser.add_argument('--output', dest='weather_file', help='output path')

args = vars(parser.parse_args())

# read data
ini_df = pd.read_csv(args['input_file'])
ini_df['state code'] = ini_df['state code'].fillna('null')

# define browser
def get_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('blink-settings=imagesEnabled=false')
    browser = webdriver.Chrome(options=options,  executable_path=args['browsername'])
    return browser

# set website parameters
def get_url(country, state, city, day, month, year):
    """
    Takes in variables to create a valid url
    """
    if country == 'US':
        lookup_URL = 'http://www.wunderground.com/history/daily/{}/{}/{}/date/{}-{}-{}'
        formatted_url = lookup_URL.format(country, state, city, year, month, day)
    else:
        lookup_URL = 'http://www.wunderground.com/history/daily/{}/{}/date/{}-{}-{}'
        formatted_url = lookup_URL.format(country, city, year, month, day)
    return formatted_url

def parse_page(url, browser):
    """
    Scrapes the web page specified by url and passes the resulting HTML
    to a Beautiful Soup Object.
    """
    try:
        browser.get(url)
        sleep(5)
    except WebDriverException:
        browser.get(url)
        sleep(5)
    html = browser.page_source
    sleep(5)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    try:
        history_table = soup.find_all('tbody')[1]
    except:
        return None
    return soup

def scrape_the_underground(url, browser):
    i = 0
    soup = parse_page(url, browser)

    while(soup is None):
        i += 1
        print('times of trying:' + str(i))
        sleep(5)
        soup = parse_page(url, browser)
        if i > 1:
            soup = 'stop'
    return soup

# Retrieve temperature data
def get_tmp_data(soup, current_date):
    if soup == 'stop':
        temperature_dict = {}
    else:
        history_table = soup.find_all('tbody')[-1]
        history_table_rows = history_table.findAll('tr')
        temperature_dict = dict()
        lyst_tmp = [] # temperature
        lyst_humi = [] # humidity
        lyst_des = [] # weather condition
        for row in history_table_rows:
            temperature_dict['date'] = current_date.strftime('%d.%m.%Y')
            cells = row.findAll('td')
            # calculate day average temperature
            tmp_0 = cells[1].get_text().strip()
            tmp_0 = int(tmp_0.encode('unicode-escape').decode('string_escape').replace('\xa0F',''))
            lyst_tmp.append(tmp_0)
            temperature_dict['Actual Mean Temperature'] = np.mean(lyst_tmp)
            # calculate day average humidity
            tmp_1 = cells[3].get_text().strip()
            tmp_1 = int(tmp_1.encode('unicode-escape').decode('string_escape').replace('\xa0%',''))
            lyst_humi.append(tmp_1)
            temperature_dict['Actual Mean Humidity'] = np.mean(lyst_humi)/100
            # collect weather condition
            tmp_2 = cells[-1].get_text().strip()
            tmp_2 = tmp_2.encode('unicode-escape').decode('string_escape')
            lyst_des.append(tmp_2)
            temperature_dict['weather condition'] = lyst_des
    return temperature_dict

browser = get_browser()
dict_list = []
with open(args['weather_file'], 'w+') as out_file:
    out_file.write('date, country code, city, actual_mean_temp, actual_mean_humidity, weather condition\n')


def obtain_weather(mydf):
    c_date = datetime.strptime(mydf['date'], '%d.%m.%Y')
    full_url = get_url(mydf['country code'],
                        mydf['state code'],
                        mydf['city'],
                        c_date.day,
                        c_date.month,
                        c_date.year)

    try:
        soup = scrape_the_underground(full_url, browser)
        temperature_dict = get_tmp_data(soup, c_date)
    except Exception:
        sleep(5)
        soup = scrape_the_underground(full_url, browser)
        temperature_dict = get_tmp_data(soup, c_date)
    dict_list.append(temperature_dict)
    mydf['weather_dict'] = temperature_dict
    with open(args['weather_file'], 'a+') as f:
        f_csv = csv.writer(f)
        try:
            f_csv.writerow([temperature_dict['date'],
                           mydf['country code'],
                           mydf['city'],
                           temperature_dict['Actual Mean Temperature'],
                           temperature_dict['Actual Mean Humidity'],
                           ','.join(temperature_dict['weather condition'])])
        except:
            f_csv.writerow([mydf['date'],
                           mydf['country code'],
                           mydf['city'],
                           'null',
                           'null',
                           'null'])


if __name__ == '__main__':
    ini_df['weather_dict'] = ini_df.apply(obtain_weather, axis=1)








