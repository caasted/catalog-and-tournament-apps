from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models import base, user, store

class Product(base.Base):
	__tablename__ = "product"
	__table_args__ = {'sqlite_autoincrement': True}

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	category = Column(String(80), nullable=False)
	description = Column(String(250))
	price = Column(String(10))
	store_id = Column(Integer, ForeignKey('store.id'))
	store = relationship(store.Store)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(user.User)

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
