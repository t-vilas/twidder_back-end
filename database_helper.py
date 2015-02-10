import sqlite3
import json
from flask import g

def connect_db():
	return sqlite3.connect("database.db")

def get_db():
	db = getattr(g, 'db', None)
	if db is None:
		db = g.db = connect_db()
	return db

def add_user(email, password, firstname, familyname, gender, city, country):
	c = get_db()
	c.execute("INSERT INTO users (email, password, firstname, familyname, gender, city, country, token) values(?, ?, ?, ?, ?, ?, ?)", (email, password, firstname, familyname, gender, city, country, ""))
	c.commit()


def get_user(email, password, token):
	c = get_db()
	print "db1"
	cursor = c.cursor()
	print email
	cursor.execute("UPDATE users SET token = ? WHERE email = ? AND password = ?", (token, email, password))
	cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
	print password
	result = [dict(id=row[0], email=row[1], firstname=row[3], familyname=row[4], gender=row[5], city=row[6], country=row[7], token=row[8]) for row in cursor.fetchall()]
	print result
	cursor.close()
	print "trtrtrtrt"
	return json.dumps(result[0])

def get_user_info(token):
	c = get_db()
	cursor = c.cursor()
	cursor.execute("SELECT * FROM users WHERE token = ?", (token, ))
	result = [dict(email=row[1], firstname=row[3], familyname=row[4], gender=row[5], city=row[6], country=row[7]) for row in cursor.fetchall()]
	cursor.close()
	return json.dumps(result[0])

def get_user_info_email(email):
	c = get_db()
	cursor = c.cursor()
	cursor.execute("SELECT * FROM users WHERE email = ?", (email, ))
	result = [dict(email=row[1], firstname=row[3], familyname=row[4], gender=row[5], city=row[6], country=row[7]) for row in cursor.fetchall()]
	cursor.close()
	return json.dumps(result[0])

def get_user_messages(token):
	c = get_db()
	cursor=c.cursor()
	cursor.execute("SELECT id FROM users WHERE token = ?", (token, ))
	userid = cursor.fetchone()
	cursor.execute("SELECT * FROM messages WHERE writer = ? OR receiver = ?", (userid, userid))
	result = [dict(writer=row[1], content=row[2], receiver=row[3]) for row in cursor.fetchall()]
	cursor.close()
	return json.dumps(result)

def get_user_messages_email(email):
	c = get_db()
	cursor=c.cursor()
	cursor.execute("SELECT id FROM users WHERE email = ?", (email, ))
	userid = cursor.fetchone()
	cursor.execute("SELECT * FROM messages WHERE writer = ? OR receiver = ?", (userid, userid))
	result = [dict(writer=row[1], content=row[2], receiver=row[3]) for row in cursor.fetchall()]
	cursor.close()
	return json.dumps(result)


def insert_user(email, password, firstname, familyname, gender, city, country, token):
	c = get_db()
	cursor = c.cursor()
	cursor.execute("INSERT INTO users (email, password, firstname, familyname, gender, city, country, token) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (email, password, firstname, familyname, gender, city, country, token))
	result = [dict(id=row[0], email=row[1], firstname=row[3], familyname=row[4], gender=row[5], city=row[6], country=row[7], token=row[8]) for row in cursor.fetchall()]
	cursor.close()
	return json.dumps(result[0])

def sign_out(token):
	c = get_db()
	cursor = c.cursor()
	cursor.execute("UPDATE users SET token = '' WHERE token = ?", (token, ))
	cursor.close()

def change_password(token, old_password, new_password):
	c =get_db()
	cursor = c.cursor()
	cursor.execute("UPDATE users SET password = ? WHERE token = ? and password = ?", (new_password, token, old_password))
	cursor.close()

def post_message(token, message, email):
	c = get_db()
	cursor=c.cursor()
	cursor.execute("SELECT id FROM users WHERE token = ?", (token, ))
	userid = cursor.fetchone()
	cursor.execute("INSERT INTO messages (writer, content, receiver) VALUES (?, ?, ?)", (userid, message, email))
	#TODO change db : email = primary key
	pass

def db_close():
	get_db().close()