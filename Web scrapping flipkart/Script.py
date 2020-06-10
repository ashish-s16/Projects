#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import bs4
import pandas as pd
import numpy as np

def phones(link):
    
    page=requests.get(link)                               #connecting with the link
    soup1=bs4.BeautifulSoup(page.content,"html.parser")
    cards=soup1.find_all("div",attrs={"class":"_1UoZlX"})
    list_page=[]
    final_list=[]
    for card in cards:
        name_div=card.find("div",attrs={"class":"_3wU53n"})
        name=name_div.text
        list_page.append(name)
        price_div=card.find("div", attrs={"class":"_2rQ-NK"})
        price=price_div.text
        list_page.append(price)
        rating_div=card.find("div", attrs={"class":"hGSR34"})
        rating=rating_div.text
        list_page.append(rating)
        final_list.append(list_page)        #list of phone name, price and rating saved
        list_page=[]
        #detail="{}  {}  {}".format(name,price,rating)
        #list_page.append(detail)
    return final_list
        
#Getting details of phone from 1st page
list_phone=[]
print(" ")
print("connecting with https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1")
print(" ")
home_url="https://www.flipkart.com/"
link="https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1"
list_phone.extend(phones(link))

# Getting details of phone from 2nd to 10th page
for i in range(2,10):
    
    list_phone.extend(phones("https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={}".format(i)))

    
def format_price(price):
    price = price[1:].split(',')
    return float("".join(price))

details = np.array(list_phone)             # Converting nested list to 2D array
Details_df = pd.DataFrame(details, columns=['Phone', 'Price', 'Rating'])   #converting array to dataframe
Details_df['Rating'] = Details_df.Rating.astype("float")
Details_df['Price'] = Details_df.Price.map(format_price)

print("Showing top 5 phones on flipkart with price between 15000 and 20000 rupee and with rating more than 4.5")
print(" ")
print(Details_df[(Details_df.Price>14999) & (Details_df.Price<20001) & (Details_df.Rating>4.2)].sort_values(by='Rating', ascending = False)[:5])

print("Enter the minimum price, maximum price and minimum rating seperated by comma (,) for custom search ")
query = input().split(",")
minn = float(query[0])-1
maxx = float(query[1])+1
rate = float(query[2])-0.1
print(Details_df[(Details_df.Price>minn) & (Details_df.Price<maxx) & (Details_df.Rating>rate)].sort_values(by='Rating', ascending = False))

