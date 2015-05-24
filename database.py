import datetime
import hashlib

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Boolean, Integer, String, DateTime

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
    is_admin = Column(Boolean)

    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = User.password_hash(password)
        self.is_admin = is_admin

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

class Organization(Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Organization %s>'%self.name

event_tags = Table('event_tags', Base.metadata,
    Column('event_id', Integer, ForeignKey('event.id')),
    Column('tag_id', Integer, ForeignKey('tag.id')),
)

class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name):
        self.name = name

class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(140))

    creation = Column(DateTime)

    start = Column(DateTime)
    end = Column(DateTime)

    organization_id = Column(Integer, ForeignKey('organization.id'))
    organization = relationship('Organization', backref='events')
    
    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship('Location', backref='events')

    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship('User', backref='events')

    tags = relationship('Tag', secondary=event_tags, backref=events)

    def __new__(cls, name, location, owner, organization, description,
                start, end):
        
        if start > end:
            raise ValueError

        if db_session.query(Event).\
            filter(Event.start < end,
                   Event.end > start,
                   Event.location == location).all():
            raise ValueError

        return super().__new__(cls, name, location, owner, organization,
                               description, start, end)

    def __init__(self, name, location, owner, organization, description,
                 start, end):
        self.name = name
        self.location = location
        self.owner = owner
        self.organization = organization
        self.description = description
        self.creation = datetime.datetime.now()
        self.start = start
        self.end = end

    def __repr__(self):
        return '<Event %s>'%self.name

Base.metadata.create_all(bind=engine)
