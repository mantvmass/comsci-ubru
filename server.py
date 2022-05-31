'''
    Copyright 2022 Phumin-DEV / Onlypond
    License:
        MIT  url: https://github.com/mantvmass/comsci-ubru/blob/main/LICENSE
'''

from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import application_set

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'comsci'
# Intialize MySQL
sql = MySQL(app)

def password_hash(password):
    try:
        return hashlib.sha256(password.encode()).hexdigest()
    except Exception:
        return False
    

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/singin', methods=['GET', 'POST'])
def singin():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            # print(request.form)
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            # Check if account exists using MySQL
            cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
            # password encode
            password = password_hash(password)
            if password == False:
                return "encode error"
            else:
                cursor.execute('SELECT * FROM `accounts` WHERE `username` = %s AND `password` = %s', (username, password,))
                # Fetch one record and return result
                account = cursor.fetchone()
                # If account exists in accounts table in out database
                if account:
                    # Create session data, we can access this data in other routes
                    session['loggedin'] = True
                    session['id'] = account['id']
                    session['username'] = account['username']
                    sql.connection.commit()
                    # send response
                    return 'success'
                else:
                    return 'Invalid username or password'
        else:
            return "data error"
    else:
        return redirect((url_for('index')))



@app.route('/singup', methods=['GET', 'POST'])
def singup():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form and 'email' in request.form and 'key' in request.form:

            print(request.form)
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            key = request.form['key']

            if key != application_set.key:
                return "Incorrect key"
            else:
                # Check if account exists using MySQL
                cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM `accounts` WHERE `username` = %s or `email` = %s', (username, email))
                account = cursor.fetchone()
                # If account exists show error and validation checks
                if account:
                    return 'Account already exists!'
                elif not username or not password or not email:
                    return  'Please fill out the form!'
                else:
                    # password encode
                    password = password_hash(password)
                    if password == False:
                        return "encode error"
                    else:
                        # Account doesnt exists and the form data is valid, now insert new account into accounts table
                        cursor.execute('INSERT INTO `accounts` (`username`, `email`, `password`) VALUES (%s, %s, %s)', (username, email, password))
                        sql.connection.commit()
                        return 'success'
        else:
            return "data error"
    else:
        return redirect((url_for('index')))



@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to home page
   return redirect(url_for('index'))


@app.route('/home')
def home():
    return "Hi {} Welcome to home".format(session['username'])



@app.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('view.html')


@app.route('/edit_text/<int:id>', methods=['GET', 'POST'])
def edit_text(id):
    return render_template('edit_text.html')


@app.route('/delete_text/<int:id>', methods=['GET', 'POST'])
def delete_text(id):
    return redirect(url_for('guestbook'))


if __name__ == '__main__':
    app.run(debug=True) # run development
    # app.run(host='00.000.000.00', port=3000) # run production / host = ip server or localhost
