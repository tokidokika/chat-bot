import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        result = requests.get(url, timeout=5)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        # print("Сетевая ошибка")
        return False


def calendar_page():
    response = get_html('https://letsportpeople.com/ru/year-2020-races_ru/')

    # bs_ = BeautifulSoup(response, 'html.parser').find_all('div', recursive=False) 
    soup = BeautifulSoup(response, 'html.parser')
    calendar = soup.find_all('div') 
    month_tag = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    monthes = []
    

    for month in calendar:
        mon = month.find('a')
        if mon:
            mont = mon.get('id')
            if mont in month_tag:
                monthes.append(mont)
    print(monthes)
                
    i = 0
    for t in calendar:
        d = {}
        id_ = t.find('a')
        if id_:
            idd = id_.get('id')
            if idd in month_tag:
                i += 1
        tag_s = t.find('strong')
        if tag_s:
            tag_strong = tag_s.text
            d['month_day'] = tag_strong
        href = t.find('a')
        if href:
            links = href.get('href')
            if links:
                d['links'] = links
            event_text = href.text
            if event_text:
                d['event_name'] = event_text
                d['month'] = monthes[i - 1]
        
           
            


calendar_page()


