import datetime, json
from flask import (Flask, g, render_template, flash, redirect, url_for, request)
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)
from flask_hashing import Hashing
from cassandra.cluster import Cluster
import random
import pokepy
import requests
import models
import forms
import os
import config



client=pokepy.V2Client()

app = Flask(__name__)


app.secret_key = config.token
salt = config.token

cluster = Cluster(['cassandra'])
session = cluster.connect()

hashing = Hashing(app)

DEBUG = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
	g.db = models.db
	g.db.connect()
	g.user = current_user

@app.after_request
def after_request(response):
	g.db.close()
	return response

@app.route('/signup', methods=('GET', 'POST'))
def signup():
	form = forms.SignUpForm()
	if form.validate_on_submit():
		flash("You've successfully registered!", "success")
		models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
		return redirect(url_for('index'))
	return render_template('signup.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
	form = forms.LoginForm()
	if form.validate_on_submit():
		try:
			user = models.User.get(models.User.email == form.email.data)
		except models.DoesNotExist:
			flash("Your email or password doesn't match!", "error")
		else:
			if hashing.check_value(user.password, form.password.data, salt):
				login_user(user)
				flash("You've been logged in. Find your poekemon!", "success")
				return redirect(url_for('index'))
			else:
				flash("Your email or password doesn't match!", "error")
	return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You've been logged out! Come back soon!", "success")
	return redirect(url_for('index'))

@app.route('/<int:user_id>/home')
@login_required
def main(user_id):
	 
	global client
	poke = random.randint(1,721)
	pokeurl_template =  'https://pokeapi.co/api/v2/pokemon/{pokemon}'
	pokeurl = pokeurl_template.format(pokemon=poke)
	print(client.get_pokemon(poke))
	resp = requests.get(pokeurl)
	print(resp.status_code)
	data= resp.json()
	data=json.dumps(data, indent=4)
	json1_data = json.loads(data)
	poke_name = (json1_data["forms"][0].get("name"))
	poke_img =  (json1_data["sprites"]["front_default"])

	#cassandra querying
	rows = session.execute( """Select * From pokemon.stats where id = {} ALLOW FILTERING """.format(str(poke)))
	for pokemon in rows:
		hp = pokemon.hp
		at = pokemon.attack
		df = pokemon.defence
		sa = pokemon.spattack
		sd = pokemon.spdefence
		sp = pokemon.speed
	todo = models.Todo.select().where(models.Todo.userid == user_id)
	return render_template('home.html', todo=todo, poke=poke_name, poke_img = poke_img, hp=hp, at=at, df=df, sa=sa, sd=sd, sp=sp)

@app.route('/<int:user_id>/browsepokemo', methods=('GET', 'POST'))
@login_required
def newTask(user_id):
	form = forms.TaskForm()
	if form.validate_on_submit():
		try:
			flash("You've added a new task!")
			models.Todo.create_task(
				title = form.title.data,
				content = form.content.data,
				priority = form.priority.data,
				date = form.date.data,
				userid = user_id,
				is_done = False
				)
			todo = models.Todo.get()
			return redirect(url_for('main', user_id=user_id))
		except AttributeError:
			raise ValueError('There is some wrong field here!')
	return render_template('new_task.html', form=form)

@app.route('/<int:user_id>/search',methods=('GET', 'POST'))
@login_required
def searchuser(user_id):

	print 'hit search'
	return str(user_id)


@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	models.initialize()
	app.run(host='0.0.0.0', port=8080)
