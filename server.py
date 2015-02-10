from flask import Flask
from flask import app, request
from flask import render_template
from flask import g
import string
import json
import hashlib
import random
import database_helper
app = Flask(__name__)


@app.route('/')
def home():
	return render_template('client.html')


@app.route('/signin', methods=['POST'])
def sign_in():
	if request.method == 'POST':
		email = request.form["siemail"]
		print "test"
		password = request.form["sipassword"]
		token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
		print password
		m = hashlib.md5()
		m.update(password)
		print m.hexdigest()
		pwd = m.hexdigest()
		result = database_helper.get_user(email, pwd, token)
		print "test3"
		return render_template("client.html", token=token)


def sign_up(email, password, firstname, familyname, gender, city, country):
	if request.method == 'POST':
		token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
		m = hashlib.md5()
		m.update(password)
		pwd = m.hexdigest()
		res = database_helper.insert_user(email, pwd, firstname, familyname, gender, city, country, token)
		print res

def sign_out(token):
	if request.method == 'POST':
		database.sign_out(token);

def change_password(token, old_password, new_password):
	if request.method == 'POST':
		m = hashlib.md5()
		m.update(old_password)
		pwd1 = m.hexdigest()
		m.update(new_password)
		pwd2 = m.hexdigest()
		database_helper.change_password(token, pwd1, pwd2)

def get_user_data_by_token(token):
	res = database_helper.get_user_info(token)
	return res

def get_user_data_by_email(token, email):
	if get_user_data_by_token(token) != None:
		res = database_helper.get_user_info_email(email)
	return res

def get_user_messages_by_token(token):
		messages = database_helper.get_user_messages(token)
		print messages
	return messages

def get_user_messages_by_email(token, email):
	if get_user_data_by_token(token) != None:
		messages = database_helper.get_user_messages_email(email)
		print messages
		return messages

def post_message(token, message, email):
	if get_user_data_by_token(token) != None:
		database_helper.post_message(token, message, email)

@app.route('/hello')
def hello_world():
    return 'Hello Flask!'


if __name__ == '__main__':
    app.run(debug=True)
