from flask import Flask, request, redirect, url_for, session, flash, render_template
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['Elizarov']
users = db['users']
app.secret_key = 'your_secret_key_here'


def login():
    error_message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username})

        if user and 'password' in user and check_password_hash(user['password'], password):
            session['fullname'] = user.get('fullname', '')
            session['team'] = user.get('team', '')
            session['is_admin'] = user.get('is_admin', False)
            if user.get('is_admin', False):
                return redirect(url_for('admin_page'))
            elif str(session['team']).find('Moder') != -1:
                return redirect(url_for('moderator_page'))
            else:
                return redirect(url_for('user_page'))
        else:
            error_message = 'Неверное имя пользователя или пароль'

    return render_template('login.html', error_message=error_message)
