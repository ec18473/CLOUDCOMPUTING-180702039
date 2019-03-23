import datetime, json
from flask import (Flask, g, render_template, flash, redirect, url_for, request)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user, login_required, current_user)
import random
import requests
import models
import forms
from flask import Flask, render_template, request, url_for
import os
import pokepy



from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('yourserver.key')
context.use_certificate_file('yourserver.crt')






app = Flask(__name__)
client=pokepy.V2Client()
poke = random.randint(1,721)

pokeurl_template =  'https://pokeapi.co/api/v2/pokemon/{pokemon}'


pokeurl = pokeurl_template.format(pokemon=poke)
print(client.get_pokemon(poke))




resp = requests.get(pokeurl)
   
print resp.status_code
data= resp.json()
data=json.dumps(data, indent=4)
json1_data = json.loads(data)
poke_name = (json1_data["forms"][0].get("name"))
poke_img =  (json1_data["sprites"]["front_default"])
print poke_name
print poke_img

