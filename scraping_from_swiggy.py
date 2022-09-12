from base64 import encode
from bs4 import BeautifulSoup
import json
import requests
import sys
import pandas as pd

# sys.stdout.reconfigure(encoding='utf-8')

import requests

headers = {
    'authority': 'www.swiggy.com',
    '__fetch_req__': 'true',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'cookie': '__SW=B8ryQmDxjt8D14p_0CLQqiir4Awag2tw; _guest_tid=6e173c56-9b1b-411a-838a-3f6061267fc2; _device_id=a6682669-75ec-18a6-8f57-2e77ad7ce873; _sid=2j25885a-243d-4a83-b3dc-27ac0ca7b5dd; fontsLoaded=1; _gcl_au=1.1.1758450616.1662972610; _ga=GA1.2.1562727421.1662972610; _gid=GA1.2.1573902211.1662972610; WZRK_G=c35560629931428e898681b8c4e4f662; userLocation={%22address%22:%22Varanasi%2C%20Uttar%20Pradesh%2C%20India%22%2C%22area%22:%22%22%2C%22deliveryLocation%22:%22%22%2C%22lat%22:25.3176452%2C%22lng%22:82.9739144}; dadl=true; order_source=Google-Sok; order_medium=CPC; order_campaign=google_search_sok_food_na_narm_order_web_m_web_clubbedcities_neev_brand_newuser_v3_ei_brand_em; _gcl_aw=GCL.1662977298.CjwKCAjwsfuYBhAZEiwA5a6CDP0Kjoj9F5f-_CaH12dJIAMMMlNza0Thcz4sICooNW2FnbykqqhnbRoCXe8QAvD_BwE; _gac_0=1.1662977299.CjwKCAjwsfuYBhAZEiwA5a6CDP0Kjoj9F5f-_CaH12dJIAMMMlNza0Thcz4sICooNW2FnbykqqhnbRoCXe8QAvD_BwE; WZRK_S_W86-ZZK-WR6Z=%7B%22p%22%3A2%2C%22s%22%3A1662979065%2C%22t%22%3A1662979203%7D; _gat_UA-53591212-4=1',
    'referer': 'https://www.swiggy.com/city/pune?page=2',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

params = (
    ('page', '1'),
    ('ignoreServiceability', 'true'),
    ('lat', '18.5362'),
    ('lng', ' 73.8940'),
    ('pageType', 'SEE_ALL'),
    ('sortBy', 'RELEVANCE'),
    ('page_type', 'DESKTOP_SEE_ALL_LISTING'),
)

response = requests.get('https://www.swiggy.com/dapi/restaurants/list/v5', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.swiggy.com/dapi/restaurants/list/v5?page=1&ignoreServiceability=true&lat=18.5362&lng=%2073.8940&pageType=SEE_ALL&sortBy=RELEVANCE&page_type=DESKTOP_SEE_ALL_LISTING', headers=headers)


response = response.text
data1 = json.loads(response)
page_no = data1["data"]["pages"]
# print(data2)

names = []
restaurants = []
cities = []
prices = []
ratings = []
deliveryTimes = []
page = 0

for page in range(page_no):
    headers = {
        'authority': 'www.swiggy.com',
        '__fetch_req__': 'true',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': '__SW=B8ryQmDxjt8D14p_0CLQqiir4Awag2tw; _guest_tid=6e173c56-9b1b-411a-838a-3f6061267fc2; _device_id=a6682669-75ec-18a6-8f57-2e77ad7ce873; _sid=2j25885a-243d-4a83-b3dc-27ac0ca7b5dd; fontsLoaded=1; _gcl_au=1.1.1758450616.1662972610; _ga=GA1.2.1562727421.1662972610; _gid=GA1.2.1573902211.1662972610; WZRK_G=c35560629931428e898681b8c4e4f662; userLocation={%22address%22:%22Varanasi%2C%20Uttar%20Pradesh%2C%20India%22%2C%22area%22:%22%22%2C%22deliveryLocation%22:%22%22%2C%22lat%22:25.3176452%2C%22lng%22:82.9739144}; dadl=true; order_source=Google-Sok; order_medium=CPC; order_campaign=google_search_sok_food_na_narm_order_web_m_web_clubbedcities_neev_brand_newuser_v3_ei_brand_em; _gcl_aw=GCL.1662977298.CjwKCAjwsfuYBhAZEiwA5a6CDP0Kjoj9F5f-_CaH12dJIAMMMlNza0Thcz4sICooNW2FnbykqqhnbRoCXe8QAvD_BwE; _gac_0=1.1662977299.CjwKCAjwsfuYBhAZEiwA5a6CDP0Kjoj9F5f-_CaH12dJIAMMMlNza0Thcz4sICooNW2FnbykqqhnbRoCXe8QAvD_BwE; WZRK_S_W86-ZZK-WR6Z=%7B%22p%22%3A2%2C%22s%22%3A1662979065%2C%22t%22%3A1662979203%7D; _gat_UA-53591212-4=1',
        'referer': 'https://www.swiggy.com/city/pune?page=2',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }

    params = (
        ('page', page),
        ('ignoreServiceability', 'true'),
        ('lat', '18.5362'),
        ('lng', ' 73.8940'),
        ('pageType', 'SEE_ALL'),
        ('sortBy', 'RELEVANCE'),
        ('page_type', 'DESKTOP_SEE_ALL_LISTING'),
    )

    response = requests.get('https://www.swiggy.com/dapi/restaurants/list/v5', headers=headers, params=params)
    response = response.text
    page += 1
    print("page no is "+str(page))
    data1 = json.loads(response)
    try: 
        data2 = data1["data"]["cards"] 
    except:
        continue
    # print(data2)
    for i in range(len(data2)):
        name = data2[i]["data"]["data"]["name"]
        restaurant = data2[i]["data"]["data"]["slugs"]["restaurant"]
        city = data2[i]["data"]["data"]["slugs"]["city"]
        price = data2[i]["data"]["data"]["costForTwoString"]
        price = int(str(price)[1:int(len(price)-8)])
        rating = data2[i]["data"]["data"]["totalRatingsString"]
        deliveryTime = data2[i]["data"]["data"]["deliveryTime"]
        print(name+" "+str(price)+" "+rating+" "+str(deliveryTime))

        names.append(name)
        restaurants.append(restaurant)
        cities.append(city)
        prices.append(price)
        ratings.append(rating)
        deliveryTimes.append(deliveryTime)


print("name : ",len(names))
print("restaurant :",len(restaurants))
print("cities : ",len(cities))
print("prices : ",len(prices))
print("ratings : ",len(ratings))
print("deliveryTime : ",len(deliveryTimes))


data = pd.DataFrame(
    {
        "name" : names,
        "restaurant" : restaurants,
        "city" : cities,
        "price" : prices,
        "rating" : ratings,
        "deliveryTime" : deliveryTimes
    }
)
    
print(data.head())
    
# Here is our required data in Pune (https://www.swiggy.com/city/pune)
print(data[data.price==min(data.price)])



