# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 00:32:48 2021

@author: Martin
"""
import os
import bcrypt
import tink
from tink import daead

database = 'database.txt'
open(database, 'w').close()

#generating salt for hashing
salt=bcrypt.gensalt()

#registering tink key for AES-SIV encryption
daead.register()
keyset_handle = tink.new_keyset_handle(daead.deterministic_aead_key_templates.AES256_SIV)
daead_primitive = keyset_handle.primitive(daead.DeterministicAead)

def hash_password(pwd,salt):
  # hashing using bcrypt 
  hashed=bcrypt.hashpw(pwd.encode('utf-8'), salt)
  return hashed

def encryption_machine(plaintext,daead_primitive):
  # encrypt using AES-SIV
  associated_data = b'context'
  ciphertext = daead_primitive.encrypt_deterministically(plaintext, associated_data)
  return ciphertext

def save_to_database(user,pwd,salt,daead_primitive):
  file = open(database, "a")
  hashed_pwd=hash_password(pwd,salt)
  encrypted_pwd=encryption_machine(hashed_pwd,daead_primitive)
  file.write(f"{user}, {encrypted_pwd}\n")
  file.close()
  
def check_password(user, pwd,salt,daead_primitive):
  file = open(database, "r")
  lines=file.readlines()
  encrypted_pwd=encryption_machine(hash_password(pwd,salt),daead_primitive)
  for line in lines:
      sep=line.split(", ")
      if sep[0]==user:
      	if sep[1]==f"{encrypted_pwd}\n":
      		return True
  return False
  
#program loop
os.system('clear')
while  True:
	print("Enter 'r' to register new user/password")
	print("Enter 'l' to check authentification")
	print("Enter 'x' to quit (database will be erased) ")
	action=input(">>> ")
	os.system('clear')
	if action == "r":
		print("Register new user/pwd")
		user=input('username: ')
		pwd=input('password: ')
		save_to_database(user,pwd,salt,daead_primitive)
	if action == "l":
		print("Check authentification")
		user=input('username: ')
		pwd=input('password: ')
		verif=check_password(user,pwd,salt,daead_primitive)
		print(verif)
		input()
	if action == "x":
		break;
		
	os.system('clear')
		

	
	







  


