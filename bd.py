import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        # print("Сетевая ошибка")
        return False

def main_page():
    response = get_html('https://letsportpeople.com/')
   
    soup = BeautifulSoup(response, 'html.parser')
    new_list = soup.find_all('div', class_='featured-media')
    result_list = []
    for new in new_list:
        title = new.find('a')['title']              
        url = new.find('a')['href']
        result_list.append({
            'title': title,
            'url': url
        })
    return result_list


def get_date():
    dates = main_page()
    for date in dates:
        get_title = date.get('title').split(' ')
        year = get_title[len(get_title) - 1]
        month = get_title[len(get_title) - 2]
        country = get_title[len(get_title) - 3]
        city = get_title[len(get_title) - 4]
        print(year, month, country, city)
    return year, month, country, city 


def calendar_page():
    response = get_html('https://letsportpeople.com/ru/year-2020-races_ru/')

    month_tag = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    soup = BeautifulSoup(response, 'html.parser')
    calendar = soup.find_all('div', class_='right70')
    find_h2 = soup.find_all('h2')
    for month in find_h2:
        idmonth = month.find('a')['id']
    if idmonth in month_tag:
        find_h5 = soup.find('h5')
        print(find_h5)
        for case in calendar:

            title = case.find('a')
            if title:
                title_text = title.text
                url = case.find('a')['href']
                print(url,title_text)

calendar_page()