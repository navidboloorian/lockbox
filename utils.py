import secrets
import string
import api
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

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

  return (pem_private_key.decode(), pem_public_key.decode())

def generate_password(length=32):
  alphabet = string.printable
  password = "".join(secrets.choice(alphabet) for _ in range(length))

  return password

def encrypt_password(password, public_key_string=api.get_public_key()):
  password = password.encode("utf-8")
  public_key_bytes = public_key_string.encode("utf-8")
  public_key = serialization.load_pem_public_key(public_key_bytes)

  return public_key.encrypt(
    password,
    padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  )

def decrypt_password(private_key_string, encrypted_password):
  private_key_bytes = private_key_string.encode("utf-8")
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