from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from models import *

engine = create_engine('sqlite:///productcatalog.db')
base.Base.metadata.create_all(engine)
