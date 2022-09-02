from bs4 import BeautifulSoup
import requests
from utils import makeAgeInt, makeWeightFloat

def humane_scrape(headers, dogs):

    url = 'https://www.oregonhumane.org/adopt/?type=dogs&mode=adv&weight=small'

    main_page = requests.get(url, headers=headers).text

    soup = BeautifulSoup(main_page, 'lxml')

    result_items = soup.find_all('div', class_='result-item')

    for item in result_items:
        name = item.find('span', class_='name')
        link = item.find('a', href=True)['href']
        link = 'https://www.oregonhumane.org/' + link

        pet_page = requests.get(link, headers=headers)
        soup = BeautifulSoup(pet_page.text, 'lxml')

        pet_props = soup.find('tbody')
        
        dog = {
            'location': 'Oregon Humane',
            'name': name.text,
        }

        props_tr = pet_props.find_all('tr')
        for prop in props_tr:
            key = prop.find('th').text.lower()
            value = prop.find('td').text
            if key not in ['location', 'code #', 'kennel']:
                if (key == 'age'):
                    dog[key] = makeAgeInt(value=value)
                elif (key == 'weight'):
                    dog[key] = makeWeightFloat(value=value)
                else: 
                    dog[key] = value.strip()
            
        dog['link'] = link
        dogs.append(dog)
    return dogs