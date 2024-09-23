import secrets
import string
import api
import argparse
from user_state import UserState
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

def create_arg_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument("private_key_path", help="Path to your private key.", nargs="?")
  return parser

def private_key_bytes(private_key_string):
  return private_key_string.encode("utf-8")

def does_key_match(private_key):
  password = generate_password()

  return decrypt_password(encrypt_password(password), private_key) == password

def generate_keys():
  private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
  )

  pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
  )

  pem_public_key = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
  )

  return (pem_private_key, pem_public_key)

def generate_password(length=32):
  alphabet = string.ascii_letters + string.digits + string.punctuation
  password = "".join(secrets.choice(alphabet) for _ in range(length))

  return password

def encrypt_password(password, public_key_bytes=None):
  if public_key_bytes == None: public_key_bytes = api.get_public_key()

  public_key = serialization.load_pem_public_key(public_key_bytes)
  password = password.encode("utf-8")

  return public_key.encrypt(
    password,
    padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  )

def decrypt_password(encrypted_password, private_key_bytes=None):
  if private_key_bytes == None: private_key_bytes = UserState.private_key

  private_key = serialization.load_pem_private_key(
    private_key_bytes, 
    password=None,
    backend=default_backend()
  )

  return private_key.decrypt(
    encrypted_password,
    padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  ).decode("utf-8")

def set_private_key(private_key):
  UserState.set_private_key(private_key)