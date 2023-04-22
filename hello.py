from flask import Flask, render_template,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#create a flask instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#Secret key
app.config['SECRET_KEY'] = 'secretkey'

#Initialize the DB
db = SQLAlchemy(app)

#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create string 
    def __repr__(self):
        return '<Name> %r' %self.name

with app.app_context():
        db.create_all()


#Creating a form class
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/user/add', methods = ['GET', 'POST'])
def add_user():
    name=None
    form = UserForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data= ''
        flash("User added successfully.")
    our_users=Users.query.order_by(Users.date_added)
    return render_template('add_user.html',
                           form=form,
                           name=name,
                           our_users=our_users)


#create a route decorator
@app.route('/')
def index():
    fname = "Pradeep"
    stuff = "This is <strong>Bold</strong>"
    numbers = [1,2,3,4,5,6,7,8,9]
    return render_template('index.html', fname=fname,stuff=stuff,numbers=numbers)#


#localhost:5000/user/john
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)


#create custom error pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


#Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('505.html'), 500

@app.route('/name', methods = ['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    #Validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form submitted successfully")
    return render_template('name.html', name=name, form=form)




if __name__ == '__main__':
    app.run(debug=True)