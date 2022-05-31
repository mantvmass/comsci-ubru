
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'comsci'
# Intialize MySQL
sql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/singin', methods=['GET', 'POST'])
def singin():
    if request.method == 'POST':
        pass
    else:
        return redirect(url_for('/'))


@app.route('/singup', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST':
        pass
    else:
        return redirect(url_for('/'))


@app.route('/home')
def home():
    return render_template('test.html')


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
