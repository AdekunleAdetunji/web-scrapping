import lxml, re, requests
from bs4 import BeautifulSoup

def arrow(path):
    '''function that returns links to each movie page'''
    reqObj = requests.get(path)
    soup = BeautifulSoup(reqObj.text, 'lxml')
    tags = soup.find_all('td', attrs={'class':'titleColumn'})
    links = [tag.find('a')['href'] for tag in tags]
    return links

def info(path):
    '''function to extract all info from any movie page'''
    reqObj = requests.get(f'https://imdb.com{path}')
    soup = BeautifulSoup(reqObj.text, 'lxml')
    info = {}

    #movie title
    title = soup.find('h1', attrs={'data-testid':'hero-title-block__title'})
    info['title'] = title.string

    #tag elements holding year and rating info
    year_tag, rating_tag = soup.find_all('span', class_='sc-8c396aa2-2 itZqyK')
    year, rating = (year_tag.string, rating_tag.string)
    info['year'], info['age_rating'] = year, rating

    #sel_1 and sel_2 elements holding the director, writer and stars names
    sel_1 = soup.select('#__next > main > div > section.ipc-page-background.ip'\
                        'c-page-background--base.sc-ca85a21c-0.efoFqn > sectio'\
                        'n > div:nth-child(4) > section > section > div.sc-2a8'\
                        '27f80-2.kqTacj > div.sc-2a827f80-10.fVYbpg > div.sc-2'\
                        'a827f80-4.bWdgcV > div.sc-fa02f843-0.fjLeDR')

    sel_2 = soup.select('#__next > main > div > section.ipc-page-background.ip'\
                        'c-page-background--base.sc-ca85a21c-0.efoFqn > sectio'\
                        'n > div:nth-child(4) > section > section > div.sc-2a8'\
                        '27f80-6.jXSdID > div.sc-2a827f80-10.fVYbpg > div.sc-2'\
                        'a827f80-8.indUzh > div.sc-fa02f843-0.fjLeDR')

    #conditional as their are two different movie page structure
    if not sel_1:
        sel_1 = sel_2

    rows = sel_1[0].findChildren('li', role=True, class_='ipc-metadata-list__'\
                                 'item')
    c = 'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__li'\
        'st-content-item--link'
    dir_tags = rows[0].findChildren('a')
    writers_tags = rows[1].findChildren('a', class_ = c)
    stars_tags = rows[2].findChildren('a', class_ = c)

    info['directors'] = [name.string for name in dir_tags][0]
    info['writers'] = [name.string for name in writers_tags]
    info['stars'] = [name.string for name in stars_tags]

    #tag elements holding the movie ratings
    info['movie_rating'] = soup.find('span',
                                    class_="sc-7ab21ed2-1 jGRxWM").string
    info['total_raters'] = soup.find('div',
                                    class_="sc-7ab21ed2-3 dPVcnq").string
    return info

def dataset():
    '''function to download all movies found on the movie list page'''
    links = arrow()
    movie_infos = []
    for movie_link in links:
        try:
            movie_info = info(movie_link)
            print(movie_info)
            movie_infos.append(movie_info)
        except Exception as e:
            movie_info.append('Error')
            continue
    return movie_infos
