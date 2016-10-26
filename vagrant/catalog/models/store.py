from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models import base, user

class Store(base.Base):
	__tablename__ = 'store'
	__table_args__ = {'sqlite_autoincrement': True}

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(user.User)

	@property
	def serialize(self):
		"""Return store type object data in easily serializeable format"""
		return {
			'id': self.id, 
			'name': self.name, 
			'user_id': self.user_id, 
		}
