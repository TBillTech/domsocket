#!/usr/bin/python
"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import pickle
import hashlib

username = raw_input('Enter username: ')
import getpass
password = None
again = 'wrong'
while again != password:
    password = getpass.getpass('Enter password: ')
    again = getpass.getpass('ReEnter password: ')

def load_pickle_file(filename):
    with open(filename, 'r') as password_pickle:
        return pickle.load(password_pickle)
    
def get_passwords():
    try:
        return load_pickle_file('passwords.pkl')
    except IOError as e:
        return dict()

def write_pickle_file(filename, data):
    with open(filename, 'w+') as password_pickle:
        pickle.dump(data, password_pickle)

def write_passwords(passwords):
    write_pickle_file('passwords.pkl', passwords)

def get_provided_hashed_password(username, password):
    m = hashlib.sha256()
    m.update('%s.%s' % (username, password))
    return m.hexdigest().upper()

passwords = get_passwords()
passwords[username] = get_provided_hashed_password(username, password)
write_passwords(passwords)

print('Password for user %s successfully set!' % (username,))
