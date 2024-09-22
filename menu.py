from getpass import getpass

import pyperclip
import api
import utils
import os

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

    print(f"\nYour password is {password}, it's been copied to your clipboard!")

    api.create_entry(service, email, encrypted_password, alias)

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

    print(private_key)

    api.create_user(hash(password), public_key)

    input("Press ENTER if you've copied your private key and are ready to proceed to Lockbox: ")

    self.show()




