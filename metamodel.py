import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.types import AbstractType, Integer
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.attributes import QueryableAttribute
from flask import request

class SessionProxy(object):
	def __getattr__(self, name):
		return getattr(request._session, name)
	
	def __enter__(self):
		pass

	def __exit__(self, type, value, traceback):
		if type == None:
			try:
				request._session.commit()
			except:
				request._session.rollback()
				raise
		else:
			request._session.rollback()
			raise

def createLocalSession():
	request._session = scoped_session(sessionmaker())
	request._session.configure(bind=engine)

def closeLocalSession():
	request._session.remove()

transact = SessionProxy()
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
	transact.add(obj)
	return obj

def update(self, **kwargs):
	for k, v in kwargs.items():
		setattr(self, k, v)
	return self

@classmethod
def all(cls):
	return transact.query(cls).all()

def genFilter(cls, kwargs):
	if len(kwargs) == 1:
		k, v = kwargs.items()[0]
		return getattr(cls, k) == v

	filters = []
	for k, v in kwargs.items():
		filters.append(getattr(cls, k) == v)
	return sa.and_(*filters)

@classmethod
def some(cls, **kwargs):
	filter = genFilter(cls, kwargs)
	return transact.query(cls).filter(filter).all()

@classmethod
def one(cls, **kwargs):
	filter = genFilter(cls, kwargs)
	try:
		return transact.query(cls).filter(filter).one()
	except:
		return None

def Model(cls):
	cls.create = create
	cls.update = update
	cls.all = all
	cls.some = some
	cls.one = one
	cls.relation = relation
	__models.append(cls)
	return cls

engine = None

def setup(db):
	global engine
	try:
		file('prod', 'r')
		engine = sa.create_engine(db, client_encoding='utf8')
	except:
		engine = sa.create_engine(db)
	metadata.bind = engine

	initialized = False

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
		columns.append(sa.Column('id', Integer, primary_key=True))
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
		if table.exists():
			initialized = True
	
	metadata.create_all()
	def sub(func):
		if not initialized:
			func()
	return sub

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
