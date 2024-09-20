from sqlalchemy.orm import Session
from db import engine
from models import User

def create_user(password, public_key):
  with Session(engine) as session:
    user = User(
      password=password,
      public_key=public_key
    )

    session.add(user)
    session.commit()

def user_exists():
  with Session(engine) as session:
    user = session.query(User).all()

    return len(user) > 0
