from bs4 import BeautifulSoup
import requests
from utils import makeAgeInt, makeWeightFloat

def ofosa_scrape(headers, dogs):

    url = 'https://ofosa.org/adoptable-dogs-waiting-for-a-forever-home/'

    main_page = requests.get(url, headers=headers).text

    soup = BeautifulSoup(main_page, 'lxml')

    dog_container = soup.find_all('div', class_='list-item')
    print(dog_container)

    for container in dog_container:
        name = container.find('span', class_='name')
        link = container.find('a', href=True)['href']
        # link = 'https://www.oregonhumane.org/' + link
        print(name.text)

        pet_page = requests.get(link, headers=headers)
        soup = BeautifulSoup(pet_page.text, 'lxml')

        pet_props = soup.find('tbody')
        
        dog = {
            'location': 'OFOSA',
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