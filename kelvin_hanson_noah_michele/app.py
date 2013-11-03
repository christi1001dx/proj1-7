from flask import Flask, session, redirect, request, url_for, render_template
import auth
import posts
import comments
import datetime

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/create', methods = ['GET', 'POST'])
def create():
    username = request.form['Username']
    title = request.form['Title']
    post = request.form['Post']
    date = datetime.datetime.now();
    posts.insert({'user':username, 'title':title, post:'post', 'datetime':date})
                            
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('login.html')
    username = request.form['Username']
    password = request.form['Password']
    if auth.auth(username,password):
        return redirect(url_for('home'))
    return render_template('login.html', 
                           message = 'Invalid combo')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template('register.html')
    username = request.form['Username']
    password = request.form['Password']
    cpassword = request.form['CPassword']
    if auth.exists(username):
        return render_template('register.html',
                               message='Username already exists')
    if password != cpassword:
        return render_template('register.html',
                               message='Passwords do not match')
    auth.addUser(username, password)
    return redirect(url_for('home'))

@app.route('/<user>/<title>', methods = ['GET', 'POST'])
def blog(user, title):
    blogPost = posts.getPost(user, title)
    return render_template("blogtemplate.html", name=user, bposttitle=title, post=blogPost)
           

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port =5000)
                        
                    
