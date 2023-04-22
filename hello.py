from flask import Flask, render_template

#create a flask instance
app = Flask(__name__)

#create a route decorator
@app.route('/')
def index():
    fname = "Pradeep"
    stuff = "This is <strong>Bold</strong>"
    numbers = [1,2,3,4,5,6,7,8,9]
    return render_template('index.html', fname=fname,stuff=stuff,numbers=numbers)


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

if __name__ == '__main__':
    app.run(debug=True)