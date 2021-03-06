from flask import Flask, render_template,url_for, redirect, jsonify, request, session
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from flask_pymongo import PyMongo
import os

app= Flask(__name__)

'''db name here'''
app.config["MONGO_DBNAME"] = 'mongo'

'''To connect using a driver via the standard MongoDB URI, copy and paste from mLab'''
app.config["MONGO_URI"] = 'mongodb://localhost:27017/mongo'
app.config['SECRET_KEY'] = os.urandom(24)

mongo = PyMongo(app)

#=============================================================
#From class from WTForms to handle adding and Updating database
#=============================================================
class AddForm(FlaskForm):
	name = StringField('name', validators = [InputRequired()])
	location = StringField('location', validators = [InputRequired()])
	Contact = StringField('Contact', validators = [InputRequired()])

#===============================
#List all the users at home page
#===============================
@app.route('/')
def index():
	user_list = mongo.db.users.find()
	return render_template("result.html",user_list=user_list)

#===============================
#Helper function to hande Bson
#===============================
import json
from bson import ObjectId
from bson.objectid import ObjectId
import bson 

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

#===================================
#Create Document in the collection
#===================================

@app.route('/add', methods=["GET","POST"])
def add():
	form = AddForm()
	if form.validate_on_submit():
		name_field = form.name.data
		location_field = form.location.data
		contact_field = form.Contact.data
		data = ({'name':name_field, 'location': location_field, 'Contact': contact_field})
		user = mongo.db.users
		user.insert(data)
		return JSONEncoder().encode(data)
	return render_template("add.html", form = form)

#===================================
#Updating form
#===================================

@app.route('/updateform')
def updateform():
	id = request.args.get('id')
	user = mongo.db.users
	result_id = user.find_one({'_id':ObjectId(id)})
	form = AddForm(name=result_id['name'],location=result_id['location'],Contact=result_id['Contact'])
	return render_template("update.html", form=form, id = id)

#===================================
#Updating Document in the collection
#===================================
from bson import json_util
@app.route('/update/<id>', methods=["POST"])
def update(id):
	user = mongo.db.users
	form = AddForm()
	if form.validate_on_submit():
		result = user.update({'_id':ObjectId(id)},{'$set':{'name':form.name.data, 'location': form.location.data, 'Contact': form.Contact.data}})
	return render_template("update.html",id=id,form=form)

#===================================
#deleting Document in the collection
#===================================

@app.route('/delete/<id>')
def delete(id):
	user = mongo.db.users
	delete_record = user.delete_one({'_id':ObjectId(id)})
	return redirect(url_for('index'))



if __name__=='__main__':
	app.run(debug=True)




