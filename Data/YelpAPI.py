# Yelp API for fetching data

import requests
import json
from collections import Counter

url = "https://api.yelp.com/v3/businesses/search" I
api_key = "" 
headers = {'Authorization': 'Bearer %s' % api_key}

json1 = []

params={
    "limit": 50,
    "location": "manhattan",
    "categories": "XYZ" #Insert values from the cuisines you are considering
}
response = requests.get(url, headers=headers, params=params)
businesses = response.json()['businesses']
for i in businesses:
    json1.append(i)


for _ in range(27):
    params={
        "limit": 50,
        "offset": 50,
        "location": "manhattan","categories": "XYZ" 
}
    
response = requests.get(url, headers=headers, params=params)
businesses = response.json()['businesses']
for i in businesses:
    json1.append(i)


#Additional filtration step just to confirm the values returned contain the required cuisines as their category values
names  = ['Italian','American (New)','Japanese','Chinese','Mexican']
food_vals = []
for name in names:
    json2 = []
    for i in json1:
        print(len(i))
        print(i)
        flag = False
        for j in range(len(i)):
            if i['categories'][j]['title']==name:  #Insert values from the cuisines you are considering to store
                flag = True
        if flag:
            json2.append(i)
            cuisine_name = json2 #cuisine name will keep changing for each iteration over the names
    food_vals.append(cuisine_name)

food_vals = [Italian, American, Japanese, Chinese, Mexican]

final_data = Mexican + Italian + Japanese + Chinese + American

json_data = json.dumps(final_data)

#Create json file with all the cuisine details
with open('restaurant_details.json', 'w') as f:
    f.write(json_data)

from google.colab import files
files.download('restaurant_details.json')
