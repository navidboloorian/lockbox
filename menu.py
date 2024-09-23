from getpass import getpass

import pyperclip
import api
import utils
import os
from globals import QueryField

class Menu:
  def __init__(self):
    pass

  def show(self):

    if not api.user_exists():
      self.new_user()
    else:
      self.ui()

  def ui(self):
    while True:
      os.system("cls" if os.name == "nt" else "clear")
    
      print(
"""
1. Generate new password
2. Retrieve password
3. Replace password
4. Delete password
"""
      )

      choice = int(input("Choice: "))

      match choice:
        case 1:
          self.generate_password()
        case 2:
          self.retrieve_password()
        case 4:
          self.delete_entry()
        case _:
          print("invalid choice")

  def generate_password(self):
    service = input("\nService name: ")

    while (len(service) == 0):
      print("Service name can't be blank")
      service = input("Service name: ")

    email = input("Account email: ")

    while (len(email) == 0):
      print("Email can't be blank")
      email = input("Account email: ")

    alias = input("Alias for easy retrieval (optional): ")
    password_length = input("Password length (leave blank for 32): ")

    while (len(password_length) and not password_length.isdigit()):
      print("Password lenght must be a number")
      password_length = input("Password length (leave blank for 32): ")

    password = utils.generate_password(int(password_length) if password_length else 32)
    encrypted_password = utils.encrypt_password(password)

    pyperclip.copy(password)

    if len(alias) == 0: alias = None

    if (api.create_entry(service, email, encrypted_password, alias)): print(f"\nYour password is {password}, it's been copied to your clipboard!")

    input("\nPress ENTER to continue: ")

  def replace_password(self):
    print(
"""
Update entry by...
1. service
2. alias
3. email
"""
    )

  def delete_entry(self):
    print(
"""
Delete entry by...
1. service
2. alias
3. email
"""
    )

    choice = input("Choice: ")

    while (not choice.isdigit() or not int(choice) in range(4)):
      print("\nInput must be a number between 1 and 3.\n")
      choice = input("Choice: ")

    query_field = QueryField(int(choice))

    if (query_field == QueryField.service):
      value = input("Service: ")
    elif (query_field == QueryField.alias):
      value = input ("Alias: ")
    elif (query_field == QueryField.email):
      value = input ("Email: ")

    affected_rows = api.delete_entry(query_field, value)
    
    if affected_rows == 0:
      print("\nThere are no entries matching those parameters...")
    elif affected_rows == 1:
      print("\nEntry successfully deleted!")
    else:
      print("\nThere is more than one result, select the one you'd like: ")

      result = api.get_entry(query_field, value)

      for i in range(len(result)):
        print(f"\n{i + 1}.\nService: {result[i].service}\nAlias: {result[i].alias}\nEmail: {result[i].email}\nPassword: {utils.decrypt_password(result[i].password)}")

      value = input("\nChoice: ")

      while (not value.isdigit() or not int(value) - 1 in range(len(result))):
        print(f"\nInput must be a number between {1} and {len(result)}.\n")
        value = input("\nChoice: ")

      api.delete_entry(QueryField.id, result[int(value) - 1].id)
      print("\nEntry successfully deleted!")
    
    input("\nPress ENTER to continue: ")

  def retrieve_password(self):
    print(
"""
Retrieve by...
1. service
2. alias
3. email
"""
    )

    choice = input("Choice: ")

    while (not choice.isdigit() or not int(choice) in range(4)):
      print("\nInput must be a number between 1 and 3.\n")
      choice = input("Choice: ")

    query_field = QueryField(int(choice))

    if (query_field == QueryField.service):
      value = input("Service: ")
    elif (query_field == QueryField.alias):
      value = input ("Alias: ")
    elif (query_field == QueryField.email):
      value = input ("Email: ")

    result = api.get_entry(query_field, value)
    
    if len(result) == 0:
      print("\nThere are no results...")
    elif len(result) == 1:
      print(f"\nService: {result[0].service}\nAlias: {result[0].alias}\nEmail: {result[0].email}\nPassword: {utils.decrypt_password(result[0].password)}")
      print("\nPassword has been copied to your clipboard!")
    else:
      print("\nThere is more than one result, select the one you'd like: ")

      for i in range(len(result)):
        print(f"\n{i + 1}.\nService: {result[i].service}\nAlias: {result[i].alias}\nEmail: {result[i].email}\nPassword: {utils.decrypt_password(result[i].password)}")

      value = input("\nChoice: ")

      while (not value.isdigit() or not int(value) - 1 in range(len(result))):
        print(f"\nInput must be a number between {1} and {len(result)}.\n")
        value = input("\nChoice: ")

      result = api.get_entry(QueryField.id, result[int(value) - 1].id)
      pyperclip.copy(utils.decrypt_password(result[0].password))
      print("\nPassword has been copied to your clipboard!")
    
    input("\nPress ENTER to continue: ")

  def new_user(self):
    print(
"""
Welcome to Lockbox! To get started, please create a master password.

This will be used to access Lockbox going forward. As such, it is extremely important that you select
a secure password and that you don't share it with anyone else. Doing so can compromise your data.
"""
    )
    
    password = getpass()
    password_conf = getpass("Confirm password: ")

    while password != password_conf:
      print("\nYour passwords don't match! Try again.\n")
      password = getpass()
      password_conf = getpass("Confirm password: ")

    private_key, public_key = utils.generate_keys()

    print(
"""
You've successfully set a master password! Lockbox uses RSA encryption for passwords. In order to 
decrypt/encrypt the paswords, we need to use a private and public key pair. The public key will be 
stored and used to encrypt your data. On the other hand, the private key will not be stored. You must
copy it and have it on hand whenever you wish to use Lockbox. If you lose your private key, you will
lose access to all of your data.
"""
    )

    input("Press ENTER if you understand and are ready to access your private key: ")
    os.system("cls" if os.name == "nt" else "clear")

    print(private_key.decode())

    api.create_user(hash(password), public_key)

    input("Press ENTER if you've copied your private key and are ready to proceed to Lockbox: ")

    self.show()