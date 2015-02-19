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

@app.route('/signin/<email>/<password>', methods=['POST'])
def sign_in(email, password):
	token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
	print password
	m = hashlib.md5()
	m.update(password)
	print m.hexdigest()
	pwd = m.hexdigest()
	result = database_helper.get_user(email, pwd, token)
	jsonfile = json.dumps({"success": True, "Message": "Log in", "data": token})
	return jsonfile


@app.route('/signup/<email>/<password>/<firstname>/<familyname>/<gender>/<city>/<country>', methods=['POST'])
def sign_up(email, password, firstname, familyname, gender, city, country):
	if request.method == 'POST':
		if database_helper.get_user_info_email(email) == None:
			token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
			m = hashlib.md5()
			m.update(password)
			pwd = m.hexdigest()
			res = database_helper.insert_user(email, pwd, firstname, familyname, gender, city, country, token)
			print res
			jsonfile = json.dumps({"success": True, "Message": "New user created"})
		else : jsonfile = json.dumps({"success": False, "Message": "Already use email"})
		return jsonfile

@app.route('/signout/<token>', methods=['POST'])
def sign_out(token):
	if request.method == 'POST':
		return json.dumps({"success": True, "Message": "Log out !"})

@app.route('/passchange/<token>/<old_password>/<new_password>', methods=['POST'])
def change_password(token, old_password, new_password):
	if request.method == 'POST':
		m = hashlib.md5()
		m2 = hashlib.md5()
		m.update(old_password)
		pwd1 = m.hexdigest()
		m2.update(new_password)
		pwd2 = m2.hexdigest()
		database_helper.change_password(token, pwd1, pwd2)
		jsonfile = json.dumps({"success": True, "Message": "Password changed"})
		return jsonfile


@app.route('/userdatatoken/<token>', methods=['GET'])
def get_user_data_by_token(token):
	res = database_helper.get_user_info(token)
	if res != None:
		jsonfile = json.dumps({"success": True, "Message": "User found", "Data": res})
	else : jsonfile = json.dumps({"success": False, "Message": "Token error"})
	return jsonfile

@app.route('/userdataemail/<token>/<email>')
def get_user_data_by_email(token, email):
	if get_user_data_by_token(token) != None:
		res = database_helper.get_user_info_email(email)
		if res != None:
			jsonfile = json.dumps({"success": True, "Message": "User found", "Data": res})
		else : jsonfile = json.dumps({"success": False, "Message": "Email do not exist"})
	else : jsonfile = json.dumps({"success": False, "Message": "Token error"})
	return jsonfile

@app.route('/messages/<token>')
def get_user_messages_by_token(token):
	messages = database_helper.get_user_messages(token)
	if messages != None:
		jsonfile = json.dumps({"success": True, "Message": "messages found", "Data": messages})
	else : jsonfile = json.dumps({"success": False, "Message": "no messages"})
	return jsonfile

@app.route('/messages/<token>/<email>')
def get_user_messages_by_email(token, email):
	if get_user_data_by_token(token) != None:
		messages = database_helper.get_user_messages_email(email)
		if messages != None:
			jsonfile = json.dumps({"success": True, "Message": "messages found", "Data": messages})
		else : jsonfile = json.dumps({"success": False, "Message": "no messages"})
	else : jsonfile = json.dumps({"success": False, "Message": "token error"})
	return jsonfile

@app.route('/postmessage/<token>/<message>/<email>', methods=['POST'])
def post_message(token, message, email):
	if get_user_data_by_token(token) != None:
		message = html_escape(message)
		print message
		database_helper.post_message(token, message, email)
		jsonfile = json.dumps({"success": True, "Message": "Message send"})
	else : jsonfile = json.dumps({"success": False, "Message": "token error"})
	return jsonfile

@app.route('/hello')
def hello_world():
    return 'Hello Flask!'

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
}

def html_escape(text):
    return "".join(html_escape_table.get(c,c) for c in text)



if __name__ == '__main__':
    app.run(debug=True)
