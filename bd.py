import requests

from bs4 import BeautifulSoup

from database import Event, base, session

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

    soup = BeautifulSoup(response, 'html.parser')
    calendar = soup.find_all('div')
    
    month_tag = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    countries = {'Швейцария': 'Швейцария', 'Норвегия': 'Норвегия', 'Израиль': 'Израиль', 'Марокко': 'Марокко', 'Индия': 'Индия', 'Испания': 'Испания', 'Португалия':'Португалия', 
                'Оаэ': 'ОАЭ', 'Тайланд': 'Тайланд', 'Гонконг': 'Гонконг', 'Италия': 'Италия', 
                'Оман': 'Оман', 'Россия': 'Россия', 'Хорватия': 'Хорватия', 'Турция': 'Турция', 'Мальта': 'Мальта', 'Япония': 'Япония', 
                'Греция': 'Греция', 'Кипр': 'Кипр', 'Германия': 'Германия', 'Венгрия': 'Венгрия', 'Польша': 'Польша', 'Казахстан': 'Казахстан',
                'Австрия': 'Австрия', 'Грузия':'Грузия', 'Беларусь': 'Беларусь', 'Чехия': 'Чехия', 'Финляндия': 'Финляндия', 'Дания':'Дания', 
                'Латвия': 'Латвия', 'Швеция': 'Швеция', 'Литва': 'Литва', 'Исландия': 'Исландия', 'Словакия': 'Словакия', 'Эстония': 'Эстония', 
                'Украина': 'Украина', 'Люксембург': 'Люксембург', 'Молдова': 'Молдова', 'Великобритания': 'Великобритания', 'Сша': 'США', 
                'Нидерланды': 'Нидерланды', 'Сербия': 'Сербия', 'Юар': 'ЮАР', 'Франция': 'Франция', 'Вьетнам': 'Вьетнам'}
    monthes = []
    

    for month in calendar:
        mon = month.find('a')
        if mon:
            mont = mon.get('id')
            if mont in month_tag:
                monthes.append(mont)
                                   
    i = 0
    for t in calendar:
        d = {}   # словарь, куда записываем все нужные данные со страницы и на основании которого строится БД

        id_ = t.find('a')
        if id_:
            idd = id_.get('id')
            if idd in month_tag:
                i += 1
                
        tag_s = t.find('h5')
        if tag_s:
            tag_day = tag_s.text
            decline = t.find('s')
            if decline:
                d['decline'] = 'Отменено'
            else:
                d['decline'] = 'Без изменений'

            href = t.find('a')
            if href:
                links = href.get('href')
                if links:
                    d['links'] = links
                
                country = t.find_all('div',{'class':'right70'})[0].get_text(separator=' ')
                country1 = country.title().replace(',', '').split(' ')

                for st in country1:
                    if st in countries:
                        d['country'] = countries[st]
                    
                event_text = href.text
                if event_text:
                    if 'Календарь забегов' in event_text:
                        continue
                    else:
                        d['event_name'] = event_text
                        d['date'] = tag_day + " " + monthes[i - 1] + " 2020"

                    dist = t.find_all('strong')
                    if dist:
                        dist = dist[-1]
                        d['distance'] = dist.text   
                        d['race_type'] = 'Шоссейный' 
                        save_event(d)

        
def save_event(d):
    event_data = Event(date=d['date'], decline=d['decline'], links=d['links'], event=d['event_name'], distance=d['distance'], places=d['country'], race_type=d['race_type'])
    session.add(event_data)
    session.commit()


calendar_page()