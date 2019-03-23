# Which Pokemon are you?
A python-flask based web app leveraging on google cloud and kubernetes engine. The app is implements user based policies and requires users to sign up before using the same. It randomly chooses a pokemon and queries the cassandra database set up in the Google Cloud to collect the details of the pokemon and displays it dynamically. It also compliments the functionality by using an external pokemon api to show the image of the pokemon. 

The user access system uses hashing of user passwords in a local database using SHA256 algorithm. It can also be extended to md5, sha1, sha224, sha256, sha384, and sha512. By default, HASHING_METHOD defaults to sha256 and HASHING_ROUNDS defaults to 1.

If you are using anything less than Python 2.7.9 you will only have the guaranteed functions provided by hashlib. Python 2.7.9 or higher allows access to OpenSSL hash functions. The name you supply to HASHING_METHOD must be valid to hashlib. To get a list of valid names, supply a random string to HASHING_METHOD and check the output when initializing your application (it raises and exception), or check hashlib.algorithms for Python 2.7.8 or less, or hashlib.algorithms_available if using Python 2.7.9+


## Requirements:

* python
* pip
* peewee
* Flask
* Flask==0.11.1
* Flask-Login==0.3.2
* Flask-SQLAlchemy==2.1
* Flask-WTF==0.12
* Jinja2==2.8
* peewee==2.8.1
* WTForms==2.1
* pokepy
* Flask-hashing
* pyopenssl

## How To Install and Run the Project :


* Install the Dependencies using `pip install -r requirements.txt`.

* Run the project using `python app.py`.

* App can be viewed at `http://0.0.0.0:8080/`
