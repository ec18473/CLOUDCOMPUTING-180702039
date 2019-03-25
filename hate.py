from flask import Flask, jsonify, request
from flask_restful import Resource, Api



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



app = Flask(__name__)
api = Api(app, errors=errors) 



class multi(Resource):
    def get(self,num):
        if num < 10:
            rows = session.execute("""Select * From pokemon.stats where id = {} ALLOW FILTERING """.format(str(num)))
			for pokemon in rows:
			    name = pokemon.name
				hp = pokemon.hp
				at = pokemon.attack
				df = pokemon.defence
				sa = pokemon.spattack
				sd = pokemon.spdefence
				sp = pokemon.speed
        	return {'POKEMON': pokemon.name, 'HP':pokemon.hp, 'Attack':pokemon.attack, 'Defence':pokemon.defence, 'Spl Attack':pokemon.spattack, 'Spl Defence':pokemon.spdefence, 'Speed':pokemon.speed}

        else:
            return errors['Pokemon DOES NOT EXIST']


        


api.add_resource(multi, '/multi/<int:num>')





if __name__ == '__main__':
    app.run(debug=True)