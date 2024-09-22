import pytest
from sqlalchemy import create_engine
from api import *
from models import *

@pytest.fixture 
def engine():
  return create_engine("sqlite+pysqlite://")

@pytest.fixture
def init_db(engine):
  init_models(engine)

def test_create_user(engine, init_db):
  # check that user doesn't exist in default database
  assert user_exists(engine) == False

  create_user("Testing", "Testing", engine)
  assert user_exists(engine) == True

  # make sure the user that exists has the same public key as the one we inputted
  assert get_public_key(engine) == "Testing"