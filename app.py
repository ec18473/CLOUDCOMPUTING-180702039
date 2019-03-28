#Importing Libraries
import datetime, json
from flask import (Flask, g, render_template, flash, redirect, url_for, request)
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)
from flask_hashing import Hashing
from cassandra.cluster import Cluster
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import random
import pokepy
import requests
import models
import forms
import os
import config #Note:config.py file has to be created.


#Python Wrapper for pokemon API
client=pokepy.V2Client()

app = Flask(__name__)

#Secret key & sal hidden and imported from config.py
app.secret_key = config.token
salt = config.token
#Cassandra configuration
cluster = Cluster(['cassandra'])
session = cluster.connect()

hashing = Hashing(app)

DEBUG = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#Custom error messages
errors = {
    'Pokemon DOES NOT EXIST': {
        'message': "Sorry. POKEMON DOES NOT EXIST. Try different number",
        'status': 404,
        'For more info': "Visit pokemon support docs"
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
}


api = Api(app, errors=errors) 


#Login manager to return user credentials
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
#Signup page
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
#Login Page
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
#Logout
@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You've been logged out! Come back soon!", "success")
	return redirect(url_for('index'))
#User based session 
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
	poke_name = (json1_data["forms"][0].get("name")) #Pokemon name abstraction from api
	poke_img =  (json1_data["sprites"]["front_default"]) #Pokemon image url abstraction from api

	#cassandra querying
	rows = session.execute( """Select * From pokemon.stats where id = {} ALLOW FILTERING """.format(str(poke)))
	for pokemon in rows: #To pass the obtained information to HTML pages
		hp = pokemon.hp
		at = pokemon.attack
		df = pokemon.defence
		sa = pokemon.spattack
		sd = pokemon.spdefence
		sp = pokemon.speed
	return render_template('home.html', todo=todo, poke=poke_name, poke_img = poke_img, hp=hp, at=at, df=df, sa=sa, sd=sd, sp=sp)


@app.route('/<int:user_id>/search',methods=('GET', 'POST'))
@login_required
def searchuser(user_id):

	print 'hit search'
	return str(user_id)


@app.route('/')
def index():
	return render_template('index.html')


#Hateous implementation
class multi(Resource):
    def get(self, num):
        if num < 721: #Limiting the search to the number of pokemons in the database
            rows = session.execute("""Select * From pokemon.stats where id = {} ALLOW FILTERING """.format(str(num)))
            for pokemon in rows: #To pass the obtained information to HTML pages
                name = pokemon.name
                hp = pokemon.hp
                at = pokemon.attack
                df = pokemon.defence
                sa = pokemon.spattack
                sd = pokemon.spdefence
                sp = pokemon.speed
            return jsonify({'POKEMON': pokemon.name, 'HP': pokemon.hp, 'Attack': pokemon.attack, 
            'Defence': pokemon.defence, 'Spl Attack': pokemon.spattack,
            'Spl Defence': pokemon.spdefence, 'Speed': pokemon.speed})
        else:
            return errors['Pokemon DOES NOT EXIST']

#Dyanamic URL that returns data from as per accordingly
api.add_resource(multi, '/pokemon/<int:num>')





if __name__ == '__main__':
	models.initialize()
	app.run(host='0.0.0.0', port=8080)
