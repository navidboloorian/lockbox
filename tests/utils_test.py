import pytest
from utils import *

@pytest.fixture
def key_pair():
  return generate_keys()

def test_generate_password_default():
  password = generate_password()
  assert len(password) == 32

def test_generate_password_custom():
  password = generate_password(20)
  assert len(password) == 20

def test_encrypt_password(key_pair):
  public_key_string = key_pair[1]
  assert encrypt_password("testing", public_key_string) != "testing"

def test_decrypt_password(key_pair):
  private_key_string, public_key_string = key_pair
  encrypted_password = encrypt_password("testing", public_key_string)
  assert decrypt_password(encrypted_password, private_key_string) == "testing"