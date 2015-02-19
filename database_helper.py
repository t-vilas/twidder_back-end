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
	print token
	cursor.execute("UPDATE users SET token = ? WHERE email = ? AND password = ?", (token, email, password))
	cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
	print password
	c.commit()
	result = [dict(email=row[0], firstname=row[2], familyname=row[3], gender=row[4], city=row[5], country=row[6], token=row[7]) for row in cursor.fetchall()]
	print result
	print "trtrtrtrt"
	if cursor.execute("SELECT Count(*) FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()[0] <= 0:
		cursor.close()
		return None
	cursor.close()
	return json.dumps(result[0])

def get_user_info(token):
	c = get_db()
	cursor = c.cursor()
	cursor.execute("SELECT * FROM users WHERE token = ?", (token, ))
	result = [dict(email=row[0], firstname=row[2], familyname=row[3], gender=row[4], city=row[5], country=row[6]) for row in cursor.fetchall()]
	print result
	if cursor.execute("SELECT Count(*) FROM users WHERE token = ?", (token, )).fetchone()[0] <= 0:
		cursor.close()
		return None
	cursor.close()
	return json.dumps(result[0])

def get_user_info_email(email):
	c = get_db()
	cursor = c.cursor()
	cursor.execute("SELECT * FROM users WHERE email = ?", (email, ))
	result = [dict(email=row[0], firstname=row[2], familyname=row[3], gender=row[4], city=row[5], country=row[6]) for row in cursor.fetchall()]
	print result
	if cursor.execute("SELECT Count(*) FROM users WHERE email = ?", (email, )).fetchone()[0] <= 0:
		cursor.close()
		return None
	cursor.close()
	return json.dumps(result[0])

def get_user_messages(token):
	c = get_db()
	cursor=c.cursor()
	cursor.execute("SELECT email FROM users WHERE token = ?", (token, ))
	useremail = cursor.fetchone()
	useremail = useremail[0]
	print useremail
	cursor.execute("SELECT * FROM messages WHERE writer = ? OR receiver = ? ORDER BY id DESC", (useremail, useremail))
	result = [dict(writer=row[1], content=row[2], receiver=row[3]) for row in cursor.fetchall()]
	
	if (cursor.execute("SELECT Count(*) FROM messages WHERE writer = ? OR receiver = ?", (useremail, useremail)).fetchone()[0]) <= 0:
		cursor.close()
		print "bla"
		return None
	cursor.close()
	return json.dumps(result)

def get_user_messages_email(email):
	c = get_db()
	cursor=c.cursor()
	cursor.execute("SELECT * FROM messages WHERE writer = ? OR receiver = ? ORDER BY id DESC", (email, email))
	result = [dict(writer=row[1], content=row[2], receiver=row[3]) for row in cursor.fetchall()]
	if cursor.execute("SELECT Count(*) FROM messages WHERE writer = ? OR receiver = ?", (email, email)).fetchone()[0] <= 0:
		cursor.close()
		print "bla"
		return None
	cursor.close()
	return json.dumps(result)


def insert_user(email, password, firstname, familyname, gender, city, country, token):
	c = get_db()
	cursor = c.cursor()
	cursor.execute("INSERT INTO users (email, password, firstname, familyname, gender, city, country, token) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (email, password, firstname, familyname, gender, city, country, token))
	result = [dict(email=row[0], firstname=row[2], familyname=row[3], gender=row[4], city=row[5], country=row[6], token=row[7]) for row in cursor.fetchall()]
	c.commit()
	if cursor.rowcount <= 0:
		cursor.close()
		return None
	cursor.close()
	return json.dumps({"success" :True})

def token0(token):
	c = get_db()
	cursor = c.cursor()
	cursor.execute("UPDATE users SET token = '' WHERE token = ?", (token, ))
	cursor.close()
	c.commit()

def change_password(token, old_password, new_password):
	c =get_db()
	cursor = c.cursor()
	cursor.execute("UPDATE users SET password = ? WHERE token = ? and password = ?", (new_password, token, old_password))
	cursor.close()
	c.commit()

def post_message(token, message, email):
	c = get_db()
	cursor=c.cursor()
	cursor.execute("SELECT email FROM users WHERE token = ?", (token, ))
	useremail = cursor.fetchone()
	print useremail
	cursor.execute("INSERT INTO messages (writer, content, receiver) VALUES (?, ?, ?)", (useremail[0], message, email))
	c.commit()
	pass

def db_close():
	get_db().close()