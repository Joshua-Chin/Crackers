import hashlib

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(40))

    def __init__(self, username, password):
        self.username = username
        self.password = User.password_hash(password)

    @staticmethod
    def password_hash(password):
        return hashlib.new('sha1').update(password).hexdigest()

    def __repr__(self):
        return '<User %s>'%self.username

class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Location %s>'%self.name

class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(140))
    
    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship('Location', backref='events')

    def __init__(self, name, location, time):
        self.name = name
        self.location = catagory

Base.metadata.create_all(bind=engine)
