from selenium import webdriver
import time
import re
import itertools
import csv
import os
import sys

#####################################################################################

def mail():
    cas=str(datetime.now())
    fromaddr = '*********'
    toaddrs  = '*********'
    msg = 'Zajemanje podatkov iz strani je koncano!'


    # Credentials (if needed)
    username = '********'
    password = '********'

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
    print ("Mail poslan")

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
def zajemi (i):
    #i predstavlja od koliko ljudi bomo zajeli podatke

    url='http://www.forbes.com/profile/bill-gates/?list=billionaires'#začnemo s prvim iz seznama

    driver = webdriver.Firefox()
    driver.get(url)

    try:
        time.sleep(15)#počakamo, da se stran naloži do konca
        res=[]
        j=0
        while j<i:
            #če se slučajno vmes pojavi "Welcome screen" počakamo, da se stran naloži
            if driver.title == "Forbes Welcome":
                time.sleep(10)
            else:
                #izpišemo katero osebo obdelujemo
                print("Obdelujem {0}".format(''.join\
                                             ([x for x in itertools.takewhile\
                                               (lambda x: x!="-", driver.title)]).strip()))

                s=driver.find_elements_by_xpath("//*[@id='left_rail']/div[1]/div[1]")#zajamemo podatke
                mesto=re.findall(r'\w*' + '#' + r'\w*',s[0].text)
                ime=re.findall('(?<='+''.join(mesto).strip()+')(.*)',s[0].text)
                rezidenca=re.findall('(?<=Residence)(.*)',s[0].text)
                marstat=re.findall('(?<=Marital Status)(.*)',s[0].text)
                stotrok=re.findall('(?<=Children)(.*)',s[0].text)
                education=re.findall('(?<=Education)(.*)',s[0].text)
                izobrazba=''
                sola=''
                if education:#polje "education" razdelimo na izobrazbo in šolo
                    izobrazba=''.join(itertools.takewhile(lambda x:x!=',',education[0]))
                    sola=''.join((itertools.dropwhile(lambda x:x!=' ',itertools.dropwhile(lambda x:x!=',',education[0]))))
                res+=[{'mesto':''.join(mesto).strip(), \
                       'ime':''.join(ime).strip(), \
                       'rezidenca':''.join(rezidenca).strip(), \
                       'število otrok':''.join(stotrok).strip(), \
                       'izobrazba':izobrazba.strip(),\
                       'sola':sola.strip()}]           
                #poiščemo gumb "next", pri prvem iz seznama ni gumba "previous",
                #zato je gumb "next" na drugem mestu kot pri ostalih
                if j==0:                
                    xpath="//*[@id='right_rail']/div[2]/div/a/div"
                else:
                    xpath="//*[@id='right_rail']/div[2]/div[2]/a/div"
                try:
                    #programatično kliknemo gumb, ki naloži stran z naslednjim milijonarjem
                    driver.find_element_by_xpath(xpath).click()
                finally:
                    pass
                j+=1
    finally:
        #zapišemo tabelo 
        zapisi_tabelo\
        (res,['mesto', 'ime', 'rezidenca', 'število_otrok', 'izobrazba', 'sola'],\
        'csv-datoteke/milijonarjidod.csv')     
        mail()
        #ker zajemanje podatkov traja sem dodal še kodo, ki mi bo poslala mail, ko je zajemanje končano
        #!PRED UPORABO JE POTREBNO NASTAVITI USERNAME, PW IN USTREZNE NASLOVE, ker je to pobrisano zaradi zasebnosti
        #če nočete, da se pošiljanje izvede ta košček kode zakomentirajte
        print ("Pošiljam mail...")
        print ("Closing driver...")
        driver.quit()

