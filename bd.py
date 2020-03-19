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

def find_tag_h2():
    page = get_html('https://letsportpeople.com/ru/year-2020-races_ru/')
    soup = BeautifulSoup(page, 'html.parser')
    return soup.find_all('h2')


def find_tag_h5():
    page = get_html('https://letsportpeople.com/ru/year-2020-races_ru/')
    soup = BeautifulSoup(page, 'html.parser')
    return soup.find_all('h5')


def calendar_page():
    response = get_html('https://letsportpeople.com/ru/year-2020-races_ru/')

    month_tag = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    soup = BeautifulSoup(response, 'html.parser')
    # cross = soup.find_all('strong')

    # for crossed in cross:
    #     if crossed.find('s'):
    #         continue
        

    calendar = soup.find_all('div', attrs={"class":"right70"})
    find_h2 = find_tag_h2()
    find_h5 = find_tag_h5()

    # for event in calendar:
    #     title = event.find('a')
    #     if title:
    #         title_text = title.text
    #         url = event.find('a')['href']

    for month in find_h2:
        id_month = month.find('a')['id']
        if id_month in month_tag:
            real_month = id_month

            
    for date_month in find_h5:
        id_date = date_month.find('strong').text

calendar_page()

# def has_style_but_no_border(tag):
#     return tag.has_attr('style') and not tag.has_attr('border:none')

