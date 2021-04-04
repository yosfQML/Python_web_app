from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):
	_id = db.Column("id",db.Integer, primary_key=True)
	name = db.Column("name", db.String(100))
	text1 = db.Column("text1", db.String(100))
	text2 = db.Column("text2", db.String(100))
	text3 = db.Column("text3", db.String(100))
	text4 = db.Column("text4", db.String(100))
	text5 = db.Column("text5", db.String(100))
	text6 = db.Column("text6", db.String(100))

	def __init__(self,name,text1,text2,text3,text4,text5,text6):
		self.name=name
		self.text1=text1
		self.text2=text2
		self.text3=text3
		self.text4=text4
		self.text5=text5
		self.text6=text6

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session.permanent = True
		user = request.form["nm"]
		session["user"] = user

		found_user = users.query.filter_by(name=user).first()
		if found_user:
			session["text1"] = found_user.text1
			session["text2"] = found_user.text2
			session["text3"] = found_user.text3
			session["text4"] = found_user.text4
			session["text5"] = found_user.text5
			session["text6"] = found_user.text6
		else:
			usr = users(user,"","","","","","")
			db.session.add(usr)
			db.session.commit()

		flash("You have been logged in")
		return redirect(url_for("user"))
	else:
		if "user" in session:
			flash("Already logged in")
			return redirect(url_for("user"))

		return render_template("login.html")

@app.route("/user",methods=["POST","GET"])
def user():
	text1 = None
	text2 = None
	text3 = None
	text4 = None
	text5 = None
	text6 = None

	if "user" in session:
		user = session["user"]
		
		if request.method == "POST":
			text1 = request.form["text1"]
			session["text1"]=text1
			text2 = request.form["text2"]
			session["text2"]=text2
			text3 = request.form["text3"]
			session["text3"]=text3
			text4 = request.form["text4"]
			session["text4"]=text4
			text5 = request.form["text5"]
			session["text5"]=text5
			text6 = request.form["text6"]
			session["text6"]=text6
			
			found_user = users.query.filter_by(name=user).first()
			found_user.text1=text1
			found_user.text2=text2
			found_user.text3=text3
			found_user.text4=text4
			found_user.text5=text5
			found_user.text6=text6
			db.session.commit()
			
			flash("saved")

		else:
			if "text1" in session:
				text1 = session["text1"]
			if "text2" in session:
				text2 = session["text2"]
			if "text3" in session:
				text3 = session["text3"]
			if "text4" in session:
				text4 = session["text4"]
			if "text5" in session:
				text5 = session["text5"]
			if "text6" in session:
				text6 = session["text6"]

		return render_template("user.html", text1=text1, text2=text2, text3=text3,text4=text4, text5=text5, text6=text6)
	else:
		flash("You are not logged in")
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	flash("You have been logged out","info")
	session.pop("user", None)
	session.pop("text1", None)
	session.pop("text2", None)
	session.pop("text3", None)
	session.pop("text4", None)
	session.pop("text5", None)
	session.pop("text6", None)
	return redirect(url_for("login"))

if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)