#imports here
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import os 
import re
import wget 
from datetime import datetime
from time import sleep
from dotenv import load_dotenv
load_dotenv()

edge_options = webdriver.EdgeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
edge_options.add_experimental_option("prefs",prefs)
edge_options.add_argument('headless')
edge_options.add_argument('window-size=0x0')

#specify the path to msedgedriver.exe (download and save on your computer)
driver = webdriver.Edge('C:/Users/asus/msedgedriver.exe', options=edge_options)

title_list=[]
location_list=[]
salary_list=[]
time_list=[]
date_list=[]
car_list=[]
licence_list=[]
edu_list=[]
gender_list=[]
company_list=[]
content_list=[]
contact_list=[]
phone_list=[]
email_list=[]
i=1
while True:
    driver.get("https://www.ouedkniss.com/emploi_offres/"+str(i))
    sleep(4)
    print(i)
    soup=BeautifulSoup(driver.page_source,"html.parser")
    all_jobs=soup.find_all("div",{"class":"col-sm-6 col-md-4 col-12"})
    for job in all_jobs:
#--------------------------------------------------Out of the box------------------------------------------------------------------------        
        try:
            title=job.find("div",{"class":"px-2 pt-1 pb-2"}).find('h1').get_text()
        except:
            title='not found'
        try:
            salary=job.find("div",{"class":"px-2 pt-1 pb-2"}).find('h2').get_text()
        except:
            salary='not found'
        try:
            location=job.find("div",{"class":"px-2 pt-1 pb-2"}).find("div",{"class":"mt-2 d-flex flex-column flex-gap-1 line-height-1"}).find_all("span")[0].get_text()
        except:
            location='not found'
        try:
            time=job.find("div",{"class":"px-2 pt-1 pb-2"}).find("div",{"class":"mt-2 d-flex flex-column flex-gap-1 line-height-1"}).find_all("span")[1].get_text()
        except:
            time='not found'
#--------------------------------------------------In the box----------------------------------------------------------------------------
        driver.get('https://www.ouedkniss.com'+str(job.find('a').get('href')))
        sleep(5)
        chorba=BeautifulSoup(driver.page_source,"html.parser")
        #------------------------------------------Top informations-----------------------------------------------------------------------
        try:
            all_top=chorba.find("div",{"class":"o-announ-specs rounded-lg elevation-1 mt-4 v-card v-sheet theme--light"}).find_all("div",{"class":"row"})
            date='not found'
            car='not found'
            licence='not found'
            edu='not found'
            gender='not found'
            company='not found'
            for top in all_top:
                    if top.find("div",{"class":"py-0 grey--text text--darken-1 col-sm-3 col-5"}).get_text()==' Date ':
                        date=top.find('span').get_text()
                    elif top.find("div",{"class":"py-0 grey--text text--darken-1 col-sm-3 col-5"}).get_text()=="Véhiculé":
                        car=top.find('span').get_text()
                    elif top.find("div",{"class":"py-0 grey--text text--darken-1 col-sm-3 col-5"}).get_text()=="Permis de conduire":
                        licence=top.find('span').get_text()
                    elif top.find("div",{"class":"py-0 grey--text text--darken-1 col-sm-3 col-5"}).get_text()=="Niveau d'éducation":
                        edu=top.find('span').get_text()
                    elif top.find("div",{"class":"py-0 grey--text text--darken-1 col-sm-3 col-5"}).get_text()=="Sexe":
                        gender=top.find('span').get_text()
                    elif top.find("div",{"class":"py-0 grey--text text--darken-1 col-sm-3 col-5"}).get_text()=="Societé":
                        company=top.find('span').get_text()  
        except:
            date='not found'
            car='not found'
            licence='not found'
            edu='not found'
            gender='not found'
            company='not found'
            pass
        try:
            content=chorba.find("div",{"class":"align-left"}).get_text()
        except:
            content='not found'
        #------------------------------------------Bot informations----------------------------------------------------------------------
        try:
            contact=chorba.find("div",{"class":"mt-10"}).find("a").get_text()
        except:
            contact='not found'
        try:
            all_bot=chorba.find_all("div",{"class":"v-list-item theme--light"})
            phone='not found'
            email='not found' 
            for bot in all_bot:
                if bot.find("i").get('class')==['v-icon', 'notranslate', 'mdi', 'mdi-phone', 'theme--light']:
                    phone=[i.get_text() for i in bot.find_all("a")]
                elif bot.find("i").get('class')==['v-icon', 'notranslate', 'mdi', 'mdi-at', 'theme--light']:
                    email=[i.get_text() for i in bot.find_all("a")]
        except:
            phone='not found'
            email='not found'
            pass    
#--------------------------------------------------Append informations-------------------------------------------------------------------
        title_list.append(title)
        salary_list.append(salary)
        location_list.append(location)
        time_list.append(time)
        date_list.append(date)
        car_list.append(car)
        licence_list.append(licence)
        edu_list.append(edu)
        gender_list.append(gender)
        company_list.append(company)
        content_list.append(content)
        contact_list.append(contact)
        phone_list.append(phone)
        email_list.append(email)
#-------------------------------------------------
        df=pd.DataFrame({"title":title_list, "salary":salary_list, "location": location_list, "time": time_list, "date": date_list, 
        "car": car_list, "licence": licence_list, "edu": edu_list, "gender": gender_list, "company": company_list, "content": content_list, 
        "contact": contact_list, "phone": phone_list, "email": email_list})
        df.drop_duplicates(subset =["content","company"],keep = "first", inplace = True)
        df.to_csv("datasets/ouedkniss.csv", index=False) #change the filename here

        if time==' il y a 1 jour ':  # si on veut plus de jours on change le "nombre" et on ajoute "s" a la fin de jour
            break
    i+=1
    if time==' il y a 1 jour ':       # si on veut plus de jours on change le "nombre" et on ajoute "s" a la fin de jour
        break
        
driver.quit()