import json
from random import random

from bson import ObjectId
from flask import Flask, app, render_template
from flask import Flask, request, redirect, url_for, session, flash

from routes.login import db


def distribute():
    selected_options = request.args.get('options', '').split(',')

    # Если выбрано меньше трех опций, добавляем дополнительную ось без названия
    if len(selected_options) < 3:
        selected_options.append('')

    sliders = ''.join([
        f'<div>{option}: <input type="range" name="{option}" value="0" min="0" max="10" onchange="updateGraph()"></div>'
        if option else
        '<div></div>'
        for option in selected_options
    ])

    if request.method == 'POST':
        distributed_values = {option: int(request.form.get(option, 0)) for option in selected_options}

        total_score = sum(distributed_values.values())
        if total_score > 10:
            flash('Сумма баллов не может превышать 10.', 'error')
            return render_template('distribute.html', sliders=sliders, selected_options=selected_options)

        fullname = session.get('fullname')
        if fullname:
            options_collection = db['users']

            user_data = options_collection.find_one({"fullname": fullname})
            if user_data:
                user_competencies = user_data.get("distributed_values", {})

                if set(user_competencies.keys()) != set(selected_options):
                    options_collection.update_one(
                        {"fullname": fullname},
                        {"$unset": {"evaluations": ""}}
                    )

                options_collection.update_one(
                    {"fullname": fullname},
                    {"$set": {"distributed_values": distributed_values}}
                )

                flash('Баллы успешно распределены.', 'success')
                return redirect(url_for('user_page'))
            else:
                flash('Ошибка: пользователь не найден.', 'error')

    return render_template('distribute.html', sliders=sliders, selected_options=selected_options)