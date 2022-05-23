import bs4
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import psycopg2

link="https://www.flipkart.com/search?q=mobiles&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_1_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_1_0_na_na_na&as-pos=1&as-type=TRENDING&suggestionId=mobiles&requestId=cdd49d46-cb58-4f9e-a22f-e986cbb2b361"
page = requests.get(link)
soup = bs(page.content,'html.parser')

count=0
data = []

for containers in soup.findAll('a', class_='_1fQZEK'):
    name = containers.find('div', attrs={'class': '_4rR01T'})
    price = containers.find('div', attrs={'class': '_30jeq3 _1_WHN1'})
    rating = containers.find('div', attrs={'class': '_3LWZlK'})
    specification = containers.find('div', attrs={'class': 'fMghEO'})

    ## Splitting integrated specification into individual Memory, display, camera, battery,processor and Warranty specifications
    for col in specification:
        col = col.find_all('li', attrs={'class': 'rgWa7D'})
        memory = col[0].text
        display = col[1].text
        camera = col[2].text
        battery = col[3].text
        process = col[4].text
        warranty = col[5].text

    data.append((name.text, memory, display, camera, battery, process, warranty, price.text, rating.text))
    count = count + 1  # Increment row count

#establishing the connection
conn = psycopg2.connect( user='postgres',
                         password='password',
                         host='localhost')
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping EMPLOYEE table if already exists.
cursor.execute("DROP TABLE IF EXISTS MOBILE")

#Creating table as per requirement
sql ='''CREATE TABLE MOBILE(
   Product_Name text,
   All_Drive text,
   Display text,
   Camera text,
   Battery text,
   Processor text,
   Warrenty text,
   Price text,
   Rating text
   )'''

cursor.execute(sql)

insert_script = 'INSERT INTO MOBILE (Product_Name, All_Drive, Display, Camera, Battery, Processor, Warrenty, Price, Rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'

for record in data:
    cursor.execute(insert_script, record)
print("Data inserted successfully........")
cursor.execute('''SELECT * from MOBILE''')

result = cursor.fetchall();
print(result)
conn.commit()
conn.close()
