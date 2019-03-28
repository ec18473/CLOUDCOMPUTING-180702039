import datetime
from peewee import * #Model definition 
from flask_hashing import Hashing
from flask import (Flask, g, render_template, flash, redirect, url_for, request)
import config
# from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
salt = config.token
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
					password=hashing.hash_value(password, salt) #Generate hash of user password using salt
				)
		except IntegrityError:
			raise ValueError("User already exists")


def initialize():
	db.connect()
	db.create_tables([User, Todo], safe=True)
	db.close()


