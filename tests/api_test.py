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
  assert user_exists(engine) == False
  create_user("Testing", "Testing", engine)
  assert user_exists(engine) == True
  assert get_user(engine).public_key == "Testing"