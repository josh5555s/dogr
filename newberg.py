from bs4 import BeautifulSoup
import requests
from utils import makeAgeInt, makeWeightFloat

def newberg_scrape(headers, dogs):

    url = 'https://newberganimals.com/type/dogs/'

    main_page = requests.get(url, headers=headers).text

    soup = BeautifulSoup(main_page, 'lxml')

    pet_wraps = soup.find_all('div', class_='pet-wrap')

    for wrap in pet_wraps:
        name = wrap.find('div', class_='pet-name')
        link = wrap.find('a', href=True)['href']

        pet_page = requests.get(link, headers=headers)
        soup = BeautifulSoup(pet_page.text, 'lxml')

        pet_spec_sheets = soup.find_all('ul', class_='pet-specs')
        
        dog = {
            'location': 'Newberg',
            'name': name.text  
        }

        for spec_sheet in pet_spec_sheets:
            specs = spec_sheet.find_all('li')
            for spec in specs:
                colonIndex = spec.text.find(':')
                key = spec.text[0:colonIndex].strip().lower()
                value = spec.text[colonIndex + 1:].strip()
                if not value == 'Unknown':
                    if (key == 'age'):
                        dog[key] = makeAgeInt(value=value)
                    elif (key == 'weight'):
                        dog[key] = makeWeightFloat(value=value)
                    else: 
                        dog[key] = value.strip()
            dog['link'] = link
        dogs.append(dog)
    return dogs