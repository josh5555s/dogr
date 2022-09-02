from twilio.rest import Client
import keys

from newberg import newberg_scrape
from humane import humane_scrape
from ofosa import ofosa_scrape

client = Client(keys.account_sid, keys.auth_token)

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'}

dogs = []
dogs = newberg_scrape(headers, dogs)
dogs = humane_scrape(headers, dogs)
# dogs = ofosa_scrape(headers, dogs)

# Filters
filtered_dogs = dogs.copy()
for dog in dogs:

    min_weight = 7
    max_weight = 25
    min_age = 4
    max_age = 8

    if ( 'weight' in dog ):
        if dog['weight'] < min_weight or dog['weight'] > max_weight:
            if dog in filtered_dogs:
                filtered_dogs.remove(dog)
    
    if ( 'age' in dog ):
        if ( dog['age'] < min_age or dog['age'] > max_age):
            if dog in filtered_dogs:
                filtered_dogs.remove(dog)

    if ( 'good with dogs' in dog ):
        if ( dog['good with dogs'].lower() == 'no' ):
            if dog in filtered_dogs:
                filtered_dogs.remove(dog)


# output to sms and output.txt if changes have occured
output = ''

for dog in filtered_dogs:
    output += '\n'
    for key in dog:
        output += f'{key}: {dog[key]}\n'

f = open("output.txt", "r")

if output != f.read():
    message = client.messages.create(
        body=output,
        from_=keys.twilio_number,
        to=keys.target_number
    )
    f = open("output.txt", "w")
    f.write(output)
    f.close()
else:
    print('no change...')