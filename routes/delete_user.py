from flask import Flask, app, render_template
from flask import Flask, request, redirect, url_for, session, flash

from routes.login import db, users

def delete_user():
    if request.method == 'POST':
        username = request.form.get('username')
        users.delete_one({'username': username})
        flash('Пользователь удален', 'success')
        return redirect(url_for('admin_page'))

    # Исключаем администратора из списка пользователей
    all_users = users.find({'team': {'$ne': 'Admin'}})
    return render_template('delete_user.html', users=all_users)