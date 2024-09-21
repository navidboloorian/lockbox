from sqlalchemy.orm import Session
from db import engine
from models import User

# engine argument is used for testing
def create_user(password, public_key, engine=engine):
  with Session(engine) as session:
    user = User(
      password=password,
      public_key=public_key
    )

    session.add(user)
    session.commit()

def user_exists(engine=engine):
  with Session(engine) as session:
    user = session.query(User).all()

    return len(user) > 0

def get_user(engine=engine):
  with Session(engine) as session:
    return session.query(User).all()[0]
