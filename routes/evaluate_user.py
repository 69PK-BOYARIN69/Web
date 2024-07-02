import json
from flask import render_template, request, redirect, url_for, session
from bson import ObjectId
from routes.login import users


def evaluate_user(user_id):
    user = users.find_one({'_id': ObjectId(user_id)})
    distributed_values = user.get('distributed_values', {})
    distributed_labels = list(distributed_values.keys())
    sliders_html = ''
    for key, value in distributed_values.items():
        if key:  # Проверяем, есть ли у оси название
            sliders_html += f'<div>{key}: <input type="range" name="{key}" value="{value}" min="0" max="10" onchange="updateGraph()"></div>'
        else:
            sliders_html += '<div></div>'  # Если ось без названия, добавляем пустой div
    distributed_values_json = json.dumps(list(distributed_values.values()))

    if not user:
        return 'Пользователь не найден'

    if request.method == 'POST':
        evaluator_name = session.get('fullname', 'Неизвестный оценивающий')
        evaluated_values = {key: int(request.form.get(key, 0)) for key in request.form}
        existing_evaluation = users.find_one(
            {"_id": ObjectId(user_id), "evaluations.evaluator": evaluator_name}
        )

        total_score = sum(evaluated_values.values())
        if total_score > 10:
            return render_template('evaluate_user.html', sliders_html=sliders_html, user=user,
                                   distributed_labels=distributed_labels,
                                   distributed_values_json=distributed_values_json)

        if existing_evaluation:
            users.update_one(
                {"_id": ObjectId(user_id), "evaluations.evaluator": evaluator_name},
                {"$set": {"evaluations.$.scores": evaluated_values}}
            )
        else:
            users.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$push": {
                        "evaluations": {
                            "evaluator": evaluator_name,
                            "scores": evaluated_values
                        }
                    }
                }
            )
        return redirect(url_for('user_page'))
    return render_template('evaluate_user.html', sliders_html=sliders_html, user=user,
                           distributed_labels=distributed_labels, distributed_values_json=distributed_values_json)
