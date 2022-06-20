'''
    Copyright 2022 Phumin-DEV / Onlypond
    License:
        MIT  url: https://github.com/mantvmass/comsci-ubru/blob/main/LICENSE
'''

from email import message
from flask import Flask, current_app, jsonify, render_template, redirect, send_from_directory, url_for, request, flash, session, make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
import qrcode
import os
from datetime import datetime
from werkzeug.utils import secure_filename




def get_path(oldvalue=None, newvalue=None):
    path = os.path.dirname(os.path.abspath("server.py"))
    # path.replace(oldvalue, newvalue)
    return str(path)


app = Flask(__name__)


QRCODE_FOLDER = get_path()+'/static/image/qrcode/'
UPLOAD_FOLDER = get_path()+'/static/image/freshy/'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg'}

# print(QRCODE_FOLDER)


# config path
app.config['QRCODE_FOLDER'] = QRCODE_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306 # MariaDB dafault port 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'comsci'
# Intialize MySQL
sql = MySQL(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


def log(msg):
    print("LOG: ", msg)


@app.route('/home')
@app.route('/')
def index():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the Dashboard page
        return redirect((url_for('dashboard')))
    return render_template('index.html', bar_active=request.path)


@app.route('/blog')
def blog():
    return render_template('blog.html', bar_active=request.path)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        if 'email' in request.form and 'password' in request.form:
            # print(request.form)
            # Create variables for easy access
            email = request.form['email']
            password = request.form['password']
            # Check if account exists using MySQL
            cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
            # password encode
            password = password_hash(password)
            if password == False:
                return "encode error"
            else:
                cursor.execute('SELECT * FROM `accounts` WHERE `email` = %s AND `password` = %s', (email, password,))
                # Fetch one record and return result
                account = cursor.fetchone()
                # If account exists in accounts table in out database
                if account:
                    # Create session data, we can access this data in other routes
                    session['loggedin'] = True
                    session['id'] = account['id']
                    session['email'] = account['email']
                    session['password'] = account['password']
                    session['fullname'] = account['fullname']
                    session['is_admin'] = account['is_admin']
                    # send response
                    return 'success'
                else:
                    return 'Invalid email or password'
        else:
            return "data error"
    else:
        return redirect((url_for('index')))



@app.route('/signup', methods=['GET', 'POST'])
def singup():
    # Check if "fullname", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST':
        if 'fullname' in request.form and 'password' in request.form and 'email' in request.form and 'key' in request.form:
            # print(request.form)
            # Create variables for easy access
            fullname = request.form['fullname']
            password = request.form['password']
            email = request.form['email']
            key = request.form['key']

            cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT `key_signup` FROM `config`')
            query_key = cursor.fetchall() # return True/False

            if query_key:
                if key != query_key[0]['key_signup']:
                    return "Key doesn't match"
                else:
                    # Check if account exists using MySQL
                    cursor.execute('SELECT * FROM `accounts` WHERE `email` = "%s"'%email)
                    account = cursor.fetchone() # return True/False
                    # If account exists show error and validation checks
                    if account:
                        return 'Account already exists!'
                    elif not fullname or not password or not email or not key:
                        return  'Please fill out the form!'
                    else:
                        # password encode
                        password = password_hash(password)
                        if password == False:
                            return "encode error"
                        else:
                            # Account doesnt exists and the form data is valid, now insert new account into accounts table
                            cursor.execute('INSERT INTO `accounts` (`fullname`, `email`, `password`) VALUES (%s, %s, %s)', (fullname, email, password))
                            sql.connection.commit()
                            return 'success'
            else:
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
   session.pop('password', None)
   session.pop('fullname', None)
   # Redirect to home page
   return redirect(url_for('index'))


@app.route('/download/<type_load>/<file>')
def download(type_load, file):
    try:
        filename = str(file)+'.png'
        return send_from_directory(app.config['QRCODE_FOLDER'], path=filename, as_attachment=True)
    except FileNotFoundError:
        return redirect(url_for(404))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # print(request.path)
        cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM `sub` WHERE `id` = {}'.format(session['id']))
        data = cursor.fetchall() # return True/False
        return render_template('dashboard.html', fullname=session['fullname'], bar_active=request.path, data=data)
    # User is not loggedin redirect to login page
    return redirect(url_for('index'))


@app.route('/getdata', methods=["GET", "POST"])
def getdata():
    if request.method =="POST":
        number = request.form['number']
        cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM `sub` WHERE `number` = "{}"'.format(number))
        data = cursor.fetchone() # return True/False
        fullname = data['fullname']
        nickname = data['nickname']
        facebook_url = data['facebook_url']
        numberv = data['number']
        img_path = data['img_path']
        return jsonify(fullname=fullname, nickname=nickname, facebook_url=facebook_url ,number=numberv, img_path=img_path)


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
        return render_template('manage.html', fullname=session['fullname'], token=token, qrpath=qr_path, hint=hint, bar_active=request.path)
    # User is not loggedin redirect to login page
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        return render_template('profile.html', bar_active=request.path)
    return redirect(url_for('index'))


@app.route('/reset', methods=['POST'])
def reset():
    if 'loggedin' in session and request.method == 'POST':
        password = request.form['password']
        newpassword = request.form['newpassword']
        renewpassword = request.form['renewpassword']
        if newpassword == renewpassword:
            password = password_hash(password)
            newpassword = password_hash(newpassword)
            if password != False:
                if password == session['password']:
                    cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
                    ok = cursor.execute('UPDATE `accounts` SET `password` = "{}" WHERE `id` = {}'.format(newpassword, session['id']))
                    if ok:
                        sql.connection.commit()
                        return "success"
                else:
                    return "Invalid password"
        else:
            return "Password do not match"
        return "update error"


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
                return "Aready have infomation"
            else:
                data = str(session['fullname'])+str(session['email'])+str(timestamp())
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
            return "update error"
        else:
            return "data error"
    else:
        return redirect((url_for('index')))


@app.route('/view')
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
                if int(data['total_sub']) < int(query_total_config[0]['sub_tatol']):
                    hint = data['message']
                    token = data['token']
                    resp = make_response(render_template('view.html', hint=hint))
                    resp.set_cookie('token', token)
                    session['f_id'] = data['id']
                    return resp
                else:
                    return render_template('view.html', hint=True)
    return render_template('view.html', hint=None)


@app.route('/form', methods=['GET', 'POST'])
def form():
    token = request.cookies.get('token')
    if token == None:
        return "Cookie unknown, Please contact staff."
    else:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files and 'fullname' not in request.form and 'nickname' not in request.form and 'facebook_url' not in request.form and 'number' not in request.form:
                flash('data error')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                # set file name
                filename = secure_filename(file.filename)
                filename = filename.split(".")
                filename = filename[1]
                filename = str(timestamp())+"."+filename

                # get form infomation
                fullname = request.form['fullname']
                nickname = request.form['nickname']
                facebook = request.form['facebook_url']
                number = request.form['number']

                cursor = sql.connection.cursor(MySQLdb.cursors.DictCursor)
                status = cursor.execute(f'INSERT INTO `sub` (`id`, `fullname`, `nickname`, `save_token`, `facebook_url`, `number`, `img_path`) VALUES ("{session["f_id"]}", "{fullname}", "{nickname}", "{token}", "{facebook}", "{number}", "{filename}")')
                if status:
                    cursor.execute('SELECT `sub_tatol` FROM `config`')
                    query_total_config = cursor.fetchall() # return True/False
                    if query_total_config:
                        cursor.execute('SELECT * FROM `tokens` WHERE `token` = "{}"'.format(token))
                        data = cursor.fetchone()
                        if data:
                            if int(data['total_sub']) < int(query_total_config[0]['sub_tatol']):
                                newt = data['total_sub'] + 1
                                ok = cursor.execute(f'UPDATE `tokens` SET `total_sub` = "{newt}" WHERE `token` = "{token}"')
                                if ok:
                                    sql.connection.commit()
                                    # save file
                                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                                    session['success'] = "ok"
                                    return redirect(url_for("index"))
                                else:
                                    return "Update token error"
                            else:
                                return "Reached the maximum number"
                        else:
                            return "query token error"
                    else:
                        return "query limit error"
                else:
                    return "Insert data error"
            return "File not support, Supported files png, jpeg, jpg"
        return render_template('form.html')


@app.errorhandler(404)
def page_not_found(e):
    log(e)
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True) # run development and Auto restart
    # app.run(host='localhost', port=80) # run production / host = ip server or localhost 192.168.0.100
