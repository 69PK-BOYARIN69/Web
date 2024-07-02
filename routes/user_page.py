import json
from random import random
from statistics import mean

from bson import ObjectId
from flask import Flask, app, render_template
from flask import Flask, request, redirect, url_for, session, flash
from werkzeug.debug import console

from routes.login import users


def user_page():
    fullname = session.get('fullname', 'Гость')
    user_data = users.find_one({"fullname": fullname}, {'_id': 1, 'distributed_values': 1, 'evaluations': 1})

    if user_data:
        user_id = str(user_data['_id'])

        if 'distributed_values' in user_data:
            distributed_values = user_data['distributed_values']
            selected_options = list(distributed_values.keys())
            data_values = list(distributed_values.values())
        else:
            selected_options = ['Категория 1', 'Категория 2', 'Категория 3']
            data_values = [0, 0, 0]

        i = 0
        if 'evaluations' in user_data:
            evaluations = user_data['evaluations']
            evaluation_scores = {option: [] for option in selected_options}

            for evaluation in evaluations:
                i += 1
                scores = evaluation.get('scores', {})
                for option in selected_options:
                    if option in scores:
                        evaluation_scores[option].append(scores[option])

            average_scores = {option: round(mean(scores), 2) if scores else 0 for option, scores in
                              evaluation_scores.items()}
            average_scores = list(average_scores.values())
        else:
            average_scores = [0, 0, 0]

        average = []
        for value, score in zip(data_values, average_scores):
            avg = round((value + score * i) / (i + 1), 2)
            average.append(avg)

        return render_template('user_page.html', fullname=fullname, selected_options=selected_options,
                               data_values=data_values, average=average, average_scores=average_scores, user_id=user_id)

    else:
        return 'Пользователь не найден в базе данных.'