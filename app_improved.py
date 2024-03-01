from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta
from functools import wraps
"""
Improved with decorator for login - for a more DRY approach
"""


app = Flask(__name__)
app.secret_key = 'insertKeyHere'
app.permanent_session_lifetime = timedelta(minutes=1)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return decorated_function


# Landing page
@app.route('/')
@login_required
def start():
    return redirect(url_for('home'))


# Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session["username"] = request.form['username']
        return redirect(url_for('home'))
    elif "username" in session:
        return redirect(url_for('home'))
    else:
        return render_template('login.html')
#Login
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Home
@app.route('/home')
@login_required
def home():
    return "Welcome to Home Page - Logged in as " + session['username']




if __name__ == '__main__':
    app.run(debug=True)