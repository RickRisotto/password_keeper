#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module collects and stores user login information.
 If data is already stored shows user's credentials
"""


import sqlite3
import os
import getpass


def get_input():
    try:
        uname = input('Enter username : ')
        print('Thank you, {}! Now we need a little more...'.format(uname))
        password = getpass.getpass(prompt='Enter password : ')
        res = {uname: password}
        return res
    except getpass.GetPassWarning as gpw:
        print('make sure nobody sees you typing!', gpw)


def create_db() -> 'cr db if not exists':
    """ Check db exists creates it if otherwise """

    default_db_name = 'user_keys.db'
    db_schema = 'keychain_schema.sql'
    db_exists = os.path.exists(default_db_name)
    connect = sqlite3.connect(db_schema)
    if not db_exists:
        with open(db_schema, 'r') as file:
            schema = file.read()
            connect.executescript(schema)
    else:
        pass
    connect.close()


def check_user_exists(user_input):
    for key in user_input.keys():
        default_db_name = 'user_keys.db'
        connect = sqlite3.connect(default_db_name)
        try:
            with connect:
                query = 'insert into storage (Username) values (?)'
                connect.execute(query, (key,))
                return key
        except sqlite3.IntegrityError:
            print(" Welcome back, {} ".format(key))
        connect.close()


def check_password_exists(user_input):
    for k, value in user_input.items():
        default_db_name = 'user_keys.db'
        connect = sqlite3.connect(default_db_name)
        connect.row_factory = sqlite3.Row
        try:
            with connect:
                pw = 'Password'
                query = 'select exists (SELECT * from storage where {}=?)'.format(pw)
                res = connect.execute(query, (value, ))
                for row in res:
                    if list(row) == [0]:
                        query = 'insert into storage (Password) values (?)'
                        connect.execute(query, (value,))
                    else:
                        return value
        except sqlite3.OperationalError as oe:
            print('Looks like you have a new password...', oe)
        connect.close()


def add_new_data(user_input):
    default_db_name = 'user_keys.db'
    connect = sqlite3.connect(default_db_name)
    for key, value in user_input.items():
        try:
            with connect:
                print('adding a new data for user {}... '.format(key))
                query = 'Insert into storage (Username) values (?)'
                data = value
                connect.execute(query, (data,))
                print('Data added successfully')
                break
        except sqlite3.IntegrityError as ie:
            print('We already have this user. Please choose another username. ', ie)
    connect.close()


def main():
    create_db()
    user_input = get_input()
    us_res = check_user_exists(user_input)
    pw_res = check_password_exists(user_input)
    default_db_name = 'user_keys.db'
    connect = sqlite3.connect(default_db_name)
    for k, v in user_input.items():
        if us_res != k and pw_res == v:
            for key in user_input.keys():
                user_choice = (input('show password for user {} ? y/n '.format(key))).capitalize()
                if user_choice == 'Y':
                    query = 'select * from storage WHERE {}=?'.format('Password')
                    res = connect.execute(query, (v,))
                    print('Password for User {}'.format(key))
                    for row in res:
                        out = list(row)
                        print(out[1])
                else:
                    print('Ok...')
                    break
        else:
            add_new_data(user_input)
    connect.close()


if __name__ == '__main__':
    main()
