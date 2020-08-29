# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 16:47:00 2020

@author: P Srihari
"""

from bs4 import BeautifulSoup as soup  # Web scrapping library
from urllib.request import urlopen as uReq  # Web request library
import qrcode as qr #Qrcode library
.
page_url = "https://www.netflix.com/browse/genre/34399" #Website link

uClient = uReq(page_url) # opens the connection

page_soup = soup(uClient.read(), "html.parser") #Parse the html
uClient.close()
items = page_soup.findAll("li", {"class": "nm-content-horizontal-row-item"}) #Retreive the required tag data

fname = "movies.csv" #create the CSV file
headers = "Name,Link,Critic,User \n"
f = open(fname, "w")
f.write(headers)

for i in items: #retreive movie details
    try:
        link = (i.a["href"])
        name = (i.img["alt"])
        if (' ' in name):
            n = name.replace(' ','_')
        else:
            n = name
        pu = 'https://www.rottentomatoes.com/m/'+n 
        uClient = uReq(pu) #retreive further details in rotten tomatoes
        page_soup = soup(uClient.read(), "html.parser")
        uClient.close()
        select = page_soup.findAll("span", {"class": "mop-ratings-wrap__percentage"})
        critic = select[0].text
        critic.strip()
        user = select[1].text
        user.strip()
        f.write(name + ", " + link + ", " + critic + ", " + user + "\n") #write to csv file
        
        fn = str(name) + '.jpg'
        q = qr.make(link) #create a qr 
        q.save(fn) #save the qr
    except:
        pass
f.close()
