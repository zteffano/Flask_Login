from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'insertKeyHere'
app.permanent_session_lifetime = timedelta(minutes=1)


# Landing page
@app.route('/')
def start():
    if "username" in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

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
def home():
    if "username" in session:
        return "Welcome to Home Page - Logged in as " + session['username']
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)