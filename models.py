import datetime
from peewee import *
from flask_hashing import Hashing
from flask import (Flask, g, render_template, flash, redirect, url_for, request)

# from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

app = Flask(__name__)
hashing = Hashing(app)

db = SqliteDatabase('list.db')

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField(max_length=100)

	class Meta:
		database = db

	@classmethod	
	def create_user(cls, username, email, password):
		
		try:
			with db.transaction():
				cls.create(
					username=username,
					email=email,
					password=hashing.hash_value(password, salt)
					# password=generate_password_hash(password)
				)
		except IntegrityError:
			raise ValueError("User already exists")

class Todo(Model):
	title = CharField()
	content = CharField()
	priority = CharField()
	date = DateField()
	userid = IntegerField()
	is_done = BooleanField(default=False)

	class Meta:
		database = db

	@classmethod
	def create_task(cls, title, content, priority, date, userid, is_done):
		with db.transaction():
			cls.create(
				title=title,
				content=content,
				priority=priority,
				date=date,
				userid = userid,
				is_done = is_done
			)

def initialize():
	db.connect()
	db.create_tables([User, Todo], safe=True)
	db.close()


