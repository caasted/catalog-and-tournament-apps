from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	__table_args__ = {'sqlite_autoincrement': True}

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)

class Store(Base):
	__tablename__ = 'store'
	__table_args__ = {'sqlite_autoincrement': True}

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		"""Return store type object data in easily serializeable format"""
		return {
			'id': self.id, 
			'name': self.name, 
			'user_id': self.user_id, 
		}

class Product(Base):
	__tablename__ = "product"
	__table_args__ = {'sqlite_autoincrement': True}

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	category = Column(String(80), nullable=False)
	description = Column(String(250))
	price = Column(String(10))
	store_id = Column(Integer, ForeignKey('store.id'))
	store = relationship(Store)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		"""Return product type object data in easily serializeable format"""
		return {
			'id': self.id, 
			'name': self.name, 
			'category': self.category, 
			'description': self.description, 
			'price': self.price, 
			'store': self.store_id, 
			'user': self.user_id, 
		}

engine = create_engine('sqlite:///productcatalog.db')
Base.metadata.create_all(engine)
