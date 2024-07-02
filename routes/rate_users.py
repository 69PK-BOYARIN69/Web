from bson import ObjectId
from flask import Flask, request, redirect, url_for, session, flash, render_template

from routes.login import users


def rate_users():
    # Получаем имя текущего пользователя и команду из сессии, если они там есть
    current_username = session.get('fullname', 'Неизвестный оценивающий')
    current_team = session.get('team')

    # Находим пользователей из указанной команды, у которых есть распределенные значения
    if current_team:
        users_list = users.find({"team": current_team, "distributed_values": {"$exists": True}},
                                {'fullname': 1, 'distributed_values': 1})
    else:
        # Если команда не указана в сессии, выводим всех пользователей с распределенными значениями
        users_list = users.find({"distributed_values": {"$exists": True}}, {'fullname': 1, 'distributed_values': 1})

    users_html = ''
    for user in users_list:
        fullname = user.get('fullname', 'Неизвестный пользователь')
        # Проверяем, не является ли текущее имя пользователем из списка
        if fullname != current_username:
            user_id = str(user.get('_id'))
            users_html += (
                f'<div>'
                f'<a href="/evaluate_user/{user_id}">{fullname}</a> '
                f'(<a href="/test/{user_id}">test</a>)'
                f'</div>'
            )

    return render_template('rate_users.html', users_html=users_html)