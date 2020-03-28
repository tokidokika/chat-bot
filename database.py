import sqlalchemy
import os

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm.session import sessionmaker

# флаг echo влючает ведение лога через стандартный модуль logging. Когда он включен, мы видим все созданные SQL-запросы
engine = create_engine('sqlite:///:memory:', echo=True)

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'botapp.db')

base = declarative_base()

class Event(base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    month = Column(String, nullable=False)
    decline = Column(String, nullable=True)
    links = Column(String, unique=True, nullable=False)
    event = Column(String, nullable=False)
    day = Column(Integer, nullable=False)
    distance = Column(String, nullable=True)

    def __repr__(self):
        return '<Occasion (event="{}", links="{}")>'.format(self.event, self.links)
        
base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()
event_name = Event(event='chto', links = 'nibud')
session.add(event_name)
print(session.new)

