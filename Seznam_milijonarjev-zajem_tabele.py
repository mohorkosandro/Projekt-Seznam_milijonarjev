from selenium import webdriver
import time
import re
import itertools
import csv
import os
import sys

#################################################################################
#profesorjeva koda za shranjevanje csv-jev
def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)
def zapisi_tabelo(slovarji, imena_polj, ime_datoteke):
    print ("Zapisujem tabelo...")
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)
    print ("Zapisovanje končano")

#################################################################################

url='http://www.forbes.com/billionaires/list'

driver = webdriver.Firefox()
driver.get(url)

try:
    time.sleep(20)#počakamo, da se stran naloži do konca
    print ('{0}  (Stran naložena)'.format(driver.title))
    for i in range (100):#ko "scrolamo" po strani se nalagajo novi podatki v tabelo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #iz tabele zajamemo podatke
    rank=driver.find_elements_by_xpath("//*[@id='list-table-body']/tr/td[2]")
    name=driver.find_elements_by_xpath("//*[@id='list-table-body']/tr/td[3]")
    networth=driver.find_elements_by_xpath("//*[@id='list-table-body']/tr/td[4]")
    age=driver.find_elements_by_xpath("//*[@id='list-table-body']/tr/td[5]")
    source=driver.find_elements_by_xpath("//*[@id='list-table-body']/tr/td[6]")
    country=driver.find_elements_by_xpath("//*[@id='list-table-body']/tr/td[7]")
    res=[]
    for i in range(len(rank)):
        #počistimo besedilo, da dobimo samo premoženje brez ostalih znakov
        premozenje=''.join(itertools.takewhile(lambda x: x!=' ',networth[i].text[1:]))
        #zapis podatkov kot seznam slovarjev
        res+=[{'mesto':rank[i].text,\
               'ime':name[i].text,\
               'premozenje':premozenje,\
               'starost':age[i].text,\
               'vir premozenja':source[i].text,\
               'drzava':country[i].text}]
    #shranjevanje csv datoteke
    zapisi_tabelo(res, ['mesto', 'ime', 'premozenje', 'starost', 'vir_premozenja', 'drzava'], 'csv-datoteke/milijonarji.csv')
finally:
    print ("Zapiram brskalnik...")
    driver.quit()
    print("Končano")









