from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String)


engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Add a new user
new_user = User(name="Alice")
session.add(new_user)
session.commit()

user = session.query(User).first()
if user:
    print(f"User ID: {user.id}")
    print(f"User Name: {user.name}")
