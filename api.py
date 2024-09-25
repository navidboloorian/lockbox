from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db import engine
from models import User, Entry
from globals import QueryField

query_map = {
  QueryField.service: Entry.service,
  QueryField.alias: Entry.alias,
  QueryField.email: Entry.email,
  QueryField.id: Entry.id
}

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
    return session.query(User).count() > 0

def get_public_key(engine=engine):
  with Session(engine) as session:
    query = select(User)
    return session.execute(query).scalar_one().public_key
  
def is_unique_service_email(service, email):
  with Session(engine) as session:
    query = select(Entry).where((Entry.service == service) & (Entry.email == email))
    result = session.execute(query).scalars().all()

    return len(result) == 0
  
def is_unique_alias(alias):
  if alias == None: return True

  with Session(engine) as session:
    query = select(Entry).where(Entry.alias == alias)
    result = session.execute(query).scalars().all()

    return len(result) == 0
  
def update_entry(field, value, password, engine=engine):
  with Session(engine) as session:
    if field == QueryField.service:
      if len(get_entry(field, value)) <= 1: 
        query = update(Entry).where(Entry.service == value).values(password=password)
      else:
        return 2
    elif field == QueryField.alias:
      query = update(Entry).where(Entry.alias == value).values(password=password)
    elif field == QueryField.email:
      if len(get_entry(field, value)) <= 1: 
        query = update(Entry).where(Entry.email == value).values(password=password)
      else:
        return 2
    elif field == QueryField.id:
        query = update(Entry).where(Entry.id == value).values(password=password)

    affected_rows = session.execute(query).rowcount
    session.commit()

    return affected_rows


def create_entry(service, email, password, alias, engine=engine):
  with Session(engine) as session:
    entry = Entry(
      service=service,
      password=password,
      email=email,
      alias=alias,
    )

    if not is_unique_service_email(service, email):
      print("\nAn entry with that email and service already exists.")
      return False
    
    if not is_unique_alias(alias):
      print("\nAn entry with that alias already exists.")
      return False

    try:
      session.add(entry)
      session.commit()
      return True
    except IntegrityError as e:
      session.rollback()
      print(e.orig)
      return False

def get_entry(field, value, engine=engine):
  with Session(engine) as session:
    query = select(Entry).where(query_map[field] == value)

    return session.execute(query).scalars().all()
  
def delete_entry(field, value, engine=engine):
  with Session(engine) as session:
    if field == QueryField.service:
      if len(get_entry(field, value)) <= 1: 
        query = delete(Entry).where(Entry.service == value)
      else:
        return 2
    elif field == QueryField.alias:
      query = delete(Entry).where(Entry.alias == value)
    elif field == QueryField.email:
      if len(get_entry(field, value)) <= 1: 
        query = delete(Entry).where(Entry.email == value)
      else:
        return 2
    elif field == QueryField.id:
      query = delete(Entry).where(Entry.id == value)

    affected_rows = session.execute(query).rowcount
    session.commit()

    return affected_rows