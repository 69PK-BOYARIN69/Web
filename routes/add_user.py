import json
from random import random

from bson import ObjectId
from flask import Flask, render_template
from flask import request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from routes.login import db, users


def add_user():
    moder = False
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')
        team = request.form.get('team')

        if str(session.get('team')).split()[0] == "Moder":
            moder = True
            team = "Team1"

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        users.insert_one({
            'fullname': fullname,
            'username': username,
            'password': hashed_password,
            'team': team
        })
        flash('Пользователь добавлен', 'success')
        if session.get('team') == None:
            redirect(url_for('admin_page'))
        elif session.get('team').split()[0] != 'Moder':
            return redirect(url_for('admin_page'))
        elif moder:
            return redirect(url_for('moderator_page'))
    else:
        return render_template('add_user.html', moder=moder)
