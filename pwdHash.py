# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 00:32:48 2021

@author: Martin
"""
import bcrypt
import tink
from tink import daead

database = 'database.txt'
secret_key = 'xxx' # use Tink to generate your secret key here

def hash_password(pwd):
  # hashing using bcrypt 
  salt=bcrypt.gensalt()
  hashed=bcrypt.hashpw(pwd.encode('utf-8'), salt)
  return hashed

def encryption_machine(msg):
  # encrypt using AES-SIV
  plaintext = msg.encode('utf-8')
  associated_data = b'context'
  # Register all deterministic AEAD primitives
  daead.register()
  # 1. Get a handle to the key material.
  keyset_handle = tink.new_keyset_handle(daead.deterministic_aead_key_templates.AES256_SIV)
  # 2. Get the primitive.
  daead_primitive = keyset_handle.primitive(daead.DeterministicAead)
  # 3. Use the primitive.
  ciphertext = daead_primitive.encrypt_deterministically(plaintext, associated_data)
  return ciphertext

def save_to_database(user, pwd):
  # use a file as a database
  # format: user, hashed_password
  # for example: file.write(user, hash_password(pwd))
  file = open(database, "a")
  hashed_pwd=hash_password(pwd)
  encrypted_pwd=encryption_machine(hashed_pwd)
  file.write(f"{user}, {encrypted_pwd}\n")
  file.close()

def check_password(user, pwd):
  # read from database
  # and check for authentication
  file = open(database, "r")
  lines=file.readlines()
  for line in lines:
      sep=line.split(", ")
      if sep[0]==user:
          if sep[1]==(pwd+"\n"):
              return True
          else:
              return False
  return False