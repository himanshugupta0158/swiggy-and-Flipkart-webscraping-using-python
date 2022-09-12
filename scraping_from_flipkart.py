from urllib import response
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

url = "https://www.flipkart.com/search?q=laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&as-pos=1&as-type=RECENT&suggestionId=laptop%7CLaptops&requestId=8f04ad1b-e8f8-44ac-8e38-0a560f87efe2&as-searchtext=lap"
response = requests.get(url)
htmlcontent = response.content
soup = BeautifulSoup(htmlcontent, "html.parser")

products = []
prices = []
ratings = []
# product = soup.find('div', attrs={'class':'_4rR01T'})
# print(product.text)

for a in soup.find_all('a', href=True, attrs={'class' : '_1fQZEK'}):
    name = a.find('div', attrs={'class':'_4rR01T'})
    price = a.find('div', attrs={'class':'_30jeq3 _1_WHN1'})
    rating = a.find('div', attrs={'class':'_3LWZlK'})
    # print(rating)
    products.append(name.text)
    prices.append(price.text)
    try:
        ratings.append(rating.text)
    except:
        print("None occured")
    finally:
        ratings.append('0')

# print("product name ",len(products),"\nprice ",len(prices),"\nratings ",len(ratings))

# ratings = [i for i in ratings if i != '0']

prices = [int(str(i[1:]).replace(',','')) for i in prices ]
df = pd.DataFrame({'Product Name' : products,'Prices' : prices,'Ratings' : ratings[:24] })
print(df.head())
print(df[df.Prices==max(df.Prices)])