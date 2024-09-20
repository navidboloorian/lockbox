from getpass import getpass

import api
import utils

class Menu:
  def __init__(self):
    pass

  def show(self):
    if not api.user_exists():
      self.new_user()

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

    print(private_key)

    api.create_user(hash(password), public_key)




