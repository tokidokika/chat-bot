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
    return year, month, country, city  # ??? Возвращает только последний. Либо (если находится где и print) возвращает = ('2020.', 'полумарафоны)', '(марафоны,', 'забегов')


def calendar_page():
    response = get_html('https://letsportpeople.com/ru/year-2020-races_ru/')

    soup = BeautifulSoup(response, 'html.parser')
    calendar = soup.find_all('div', class_='right70')
    full_calendar = calendar.find_all('div', style_='width:55')
    # calendar_list = []
    for case in full_calendar:
        title = case.find('a').text
        url = case.find('a')['href']
        print(title, url)

print(calendar_page())