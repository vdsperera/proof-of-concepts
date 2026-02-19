from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Setup
Base = declarative_base()
engine = create_engine('sqlite:///ormdb.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# 2. Define a table as a Python class
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# 3. Create table in DB
Base.metadata.create_all(engine)

# 4. Add a user
new_user = User(name="Alice")
session.add(new_user)
session.commit()

# 5. Query users
all_users = session.query(User).all()
for user in all_users:
    print(f"User ID: {user.id}, Name: {user.name}")