import lxml, requests
from bs4 import BeautifulSoup


def arrow():
    '''function to open the website and direct me to the target page'''
    reObj = requests.get('https://data.gov')
    soup = BeautifulSoup(reObj.text, 'lxml')
    link = soup.select('#menu-primary-navigation > li.menu-data > a')
    return link[0]['href']


def result():
    '''function to return the number of datasets on the data page'''
    page = arrow()
    reObj = requests.get(page)
    soup = BeautifulSoup(reObj.text, 'lxml')
    selector = ('#content > div.row.wrapper > div >'+
    ' section:nth-child(1) > div.new-results')
    target = soup.select(selector)
    return target[0].string.strip()
