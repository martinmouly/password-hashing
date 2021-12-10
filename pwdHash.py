database = 'database.txt'
secret_key = 'xxx' # use Tink to generate your secret key here

def hash_password(pwd):
  # implement your scheme
  return hash

def encryption_machine(msg):
  # encrypt using AES-SIV
  return ciphertext

def save_to_database(user, pwd):
  # use a file as a database
  # format: user, hashed_password
  # for example: file.write(user, hash_password(pwd))

def check_password(user, pwd):
  # read from database
  # and check for authentication
  return false/true