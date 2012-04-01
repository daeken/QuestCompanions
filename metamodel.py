import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.types import AbstractType, Integer
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.attributes import QueryableAttribute

session = None
metadata = sa.MetaData()

__models = []

# Monkey patched into Model-decorated classes
@classmethod
def relation(cls, *args, **kwargs):
	return orm.relation(cls, *args, **kwargs)

@classmethod
def create(cls, **kwargs):
	obj = cls()
	for k, v in kwargs.items():
		setattr(obj, k, v)
	session.add(obj)
	sync.create(cls.__name__, kwargs)
	return obj

def update(self, **kwargs):
	for k, v in kwargs.items():
		setattr(self, k, v)
	sync.update(self.__class__.__name__, self.id, kwargs)
	return self

def Model(cls):
	cls.create = create
	cls.update = update
	cls.relation = relation
	__models.append(cls)
	return cls

engine = None

def reconfigure():
	global engine, session
	new = True
	if session != None and engine != None:
		engine.dispose()
		session.close()
		new = False
	session = scoped_session(sessionmaker())
	engine = sa.create_engine('sqlite:///model.db')
	session.configure(bind=engine)
	if not new:
		metadata.create_all(bind=engine)

def setup():
	reconfigure()

	for model in __models:
		name = model.__name__
		params = []
		for field in dir(model):
			value = getattr(model, field)
			if isinstance(value, PrimaryKey):
				params = [field] + params
			else:
				params.append(field)
		
		columns = []
		relations = {}
		for field in params:
			value = getattr(model, field)
			if isinstance(value, Modifier):
				columns.append(value.build(field))
				delattr(model, field)
			elif (
					isinstance(value, AbstractType) or 
					(isinstance(value, type) and issubclass(value, AbstractType))
				):
				columns.append(sa.Column(field, value))
				delattr(model, field)
			elif isinstance(value, orm.properties.RelationProperty):
				relations[field] = value
				delattr(model, field)
		
		table = sa.Table(name, metadata, *columns)
		orm.mapper(model, table, properties=relations)
	
	metadata.create_all(bind=engine)

class Modifier(object):
	pass

class PrimaryKey(Modifier):
	def __init__(self, type):
		self.type = type
	
	def build(self, name):
		return sa.Column(name, self.type, primary_key=True)

class ForeignKey(Modifier):
	def __init__(self, type, ref, *args, **kwargs):
		self.type, self.ref = type, ref
		self.args, self.kwargs = args, kwargs
	
	def build(self, name):
		return sa.Column(name, self.type, sa.ForeignKey(self.ref), *self.args, **self.kwargs)

class Nullable(Modifier):
	def __init__(self, type, *args, **kwargs):
		self.type = type
		self.args, self.kwargs = args, kwargs
	
	def build(self, name):
		return sa.Column(name, self.type, nullable=True, *self.args, **self.kwargs)

class Unique(Modifier):
	def __init__(self, type, *args, **kwargs):
		self.type = type
		self.args, self.kwargs = args, kwargs
	
	def build(self, name):
		return sa.Column(name, self.type, unique=True, *self.args, **self.kwargs)
