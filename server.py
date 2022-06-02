'''
    Copyright 2022 Phumin-DEV / Onlypond
    License:
        MIT  url: https://github.com/mantvmass/comsci-ubru/blob/main/LICENSE
'''

from email import message
from flask import Flask, current_app, render_template, redirect, send_from_directory, url_for, request, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import qrcode
import os
from datetime import datetime
from werkzeug.utils import secure_filename



QRCODE_FOLDER = 'C:/Users/MANTVMASS/Desktop/comsci/static/image/qrcode/'
ALLOWED_EXTENSION = {'png', 'jpg', 'jpeg'}



app = Flask(__name__)

# config path
app.config['QRCODE_FOLDER'] = QRCODE_FOLDER

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


def timestamp():
    # get date to create name
    dtime = datetime.now()
    dtimestamp = dtime.timestamp()
    return int(round(dtimestamp))


def generate_qr(token):
    try:
        # create name
        name = timestamp()
        # create qrcode
        data = "https://comsci-ubru.tk/view?token={}".format(token)
        qr = qrcode.QRCode(version=1, box_size=8, border=3)
        qr.add_data(data)
        qr.make(fit=True)
        image = qr.make_image(fill='black', back_color='white')
        image.save('static/image/qrcode/{}.png'.format(name))
        return str(name)
    except Exception:
        return False


def generate_token(data):
    return hashlib.sha1(data.encode("UTF-8")).hexdigest()
    

@app.route('/home')
@app.route('/')
def index():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the Dashboard page
        return redirect((url_for('dashboard')))
    return render_template('index.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
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
                    session['email'] = account['email']
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



@app.route('/signup', methods=['GET', 'POST'])
def singup():
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form and 'email' in request.form and 'key' in request.form:
            # print(request.form)
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            key = request.form['key']

            cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT `key_signup` FROM `config`')
            query_key = cursor.fetchall() # return True/False

            if query_key:
                if key != query_key[0]['key_signup']:
                    sql.connection.commit()
                    return "Key doesn't match"
                else:
                    # Check if account exists using MySQL
                    cursor.execute('SELECT * FROM `accounts` WHERE `username` = %s or `email` = %s', (username, email))
                    account = cursor.fetchone() # return True/False
                    # If account exists show error and validation checks
                    if account:
                        sql.connection.commit()
                        return 'Account already exists!'
                    elif not username or not password or not email:
                        sql.connection.commit()
                        return  'Please fill out the form!'
                    else:
                        # password encode
                        password = password_hash(password)
                        if password == False:
                            sql.connection.commit()
                            return "encode error"
                        else:
                            # Account doesnt exists and the form data is valid, now insert new account into accounts table
                            cursor.execute('INSERT INTO `accounts` (`username`, `email`, `password`) VALUES (%s, %s, %s)', (username, email, password))
                            sql.connection.commit()
                            return 'success'
            else:
                sql.connection.commit()
                return "key not found"
        else:
            return "data error"
    else:
        return redirect((url_for('index')))



@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   session.pop('username', None)
   # Redirect to home page
   return redirect(url_for('index'))



@app.route('/download/<type_load>/<file>')
def download(type_load, file):
    try:
        filename = str(file)+'.png'
        return send_from_directory(app.config['QRCODE_FOLDER'], path=filename, as_attachment=True)
    except FileNotFoundError:
        return redirect(url_for(404))

# @app.route('/test')
# def test():
#     generate_qr("1234")
#     return "io"
    # s = sql.connection.cursor(MySQLdb.cursors.DictCursor)
    # s.execute('SELECT `key_signup` FROM `config`')
    # re = s.fetchall() # return True/False
    # if re:
    #     return "me"
    # else:
    #     return "nome"
    # sql.connection.commit()
    # # if 'Phumin2002#' in re[0]['key_signup']:
    # #     return "ok"
    # print(re)
    # return re


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # print(request.path)
        return render_template('dashboard.html', username=session['username'], bar_active=request.path)
    # User is not loggedin redirect to login page
    return redirect(url_for('index'))


@app.route('/manage')
def manage():
    # Check if user is loggedin
    if 'loggedin' in session:
        # Check if tokens exists using MySQL
        cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM `tokens` WHERE `id` = {}'.format(session['id']))
        data = cursor.fetchone() # return True/False
        if data:
            token = data['token']
            qr_path = data['qr_path']
            hint = data['message']
        else:
            token = None
            qr_path = False
            hint =None
        # User is loggedin show them the home page
        return render_template('manage.html', username=session['username'], token=token, qrpath=qr_path, hint=hint, bar_active=request.path)
    # User is not loggedin redirect to login page
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('profile.html', bar_active=request.path)
    return redirect(url_for('index'))


@app.route('/create_hint', methods=['GET', 'POST'])
def create_hint():
    # Check if "hint" POST requests exist (user submitted form)
    if request.method == 'POST':
        if 'hint' in request.form and 'loggedin' in session:
            # print(request.form)
            # Create variables for easy access
            hint = request.form['hint']
            # Check if tokens exists using MySQL
            cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM `tokens` WHERE `id` = {}'.format(session['id']))
            data = cursor.fetchone() # return True/False
            if data:
                sql.connection.commit()
                return "Aready have infomation"
            else:
                data = str(session['username'])+str(session['email'])+str(timestamp())
                token = generate_token(data)
                qrcode_path = generate_qr(token)
                # print(token)
                if qrcode_path == False:
                    return "create QRcode error"
                cursor.execute('INSERT INTO `tokens` (`id`, `token`, `message`, `qr_path`) VALUES (%s, %s, %s, %s)', (session["id"], token, hint, qrcode_path))
                sql.connection.commit()
                return redirect((url_for('manage')))
        else:
            return "data error"
    else:
        return redirect((url_for('index')))


@app.route('/delete_hint', methods=['GET', 'POST'])
def delete_hint():
    if request.method == 'POST':
        if 'loggedin' in session:
            cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM `tokens` WHERE `id` = {}'.format(session['id']))
            data = cursor.fetchone() # return True/False
            if data:
                os.remove("static/image/qrcode/{}.png".format(data['qr_path']))
                ok = cursor.execute('DELETE FROM `tokens` WHERE `id` = {}'.format(session['id']))
                if ok:
                    sql.connection.commit()
                    return "success"
            sql.connection.commit()
            return "delete error"
        else:
            return "data error"
    else:
        return redirect((url_for('index')))

@app.route('/edit_hint', methods=['GET', 'POST'])
def edit_hint():
    if request.method == 'POST':
        # print(request.form)
        if 'hint' in request.form and 'loggedin' in session:
            cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM `tokens` WHERE `id` = {}'.format(session['id']))
            data = cursor.fetchone() # return True/False
            if data:
                ok = cursor.execute('UPDATE `tokens` SET `message` = "{}" WHERE `id` = {}'.format(request.form['hint'], session['id']))
                if ok:
                    sql.connection.commit()
                    return "success"
            sql.connection.commit()
            return "update error"
        else:
            return "data error"
    else:
        return redirect((url_for('index')))


@app.route('/view', methods=['GET', 'POST'])
def view():
    res = request.args
    if 'token' in res:
        get_token =  res['token']
        cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT `sub_tatol` FROM `config`')
        query_total_config = cursor.fetchall() # return True/False
        if query_total_config:
            cursor.execute('SELECT * FROM `tokens` WHERE `token` = "{}"'.format(get_token))
            data = cursor.fetchone() # return True/False
            if data:
                if data['total_sub'] <= query_total_config[0]['sub_tatol']:
                    hint = data['message']
                    token = data['token']
                    sql.connection.commit()
                    return render_template('view.html', hint=hint, token=token)
                else:
                    sql.connection.commit()
                    return render_template('view.html', hint=True, token=True)
    sql.connection.commit()
    return render_template('view.html', hint=None, token=None)


@app.errorhandler(404)
def page_not_found(e):
    # print(e)
    return render_template('404.html'), 404

if __name__ == '__main__':
    # app.run(debug=True) # run development
    app.run(host='localhost', port=3000) # run production / host = ip server or localhost
