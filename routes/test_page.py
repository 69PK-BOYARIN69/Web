import json
from random import random

from bson import ObjectId
from flask import Flask, app, render_template
from flask import Flask, request, redirect, url_for, session, flash

from data import db
from routes.login import users


def test_page(user_id):
    if request.method == 'POST':
        evaluator_fullname = session.get('fullname')
        if not evaluator_fullname:
            return 'Пользователь не аутентифицирован. <a href="/login">Войти</a>'

        scores = {}
        for question_doc in db.testText.find():
            for question in question_doc['questions']:
                question_id = question['question']
                answer = request.form.get(question_id)
                # Заменяем None на 0
                scores[question_id] = int(answer) if answer is not None else 0

        user = db.users.find_one({'_id': ObjectId(user_id)})

        if user:
            answers = user.get('answers', [])
            existing_evaluation = next(
                (evaluation for evaluation in answers if evaluation['evaluator'] == evaluator_fullname), None)
            if existing_evaluation:
                existing_evaluation['scores'] = scores
            else:
                answers.append({'evaluator': evaluator_fullname, 'scores': scores})
        else:
            answers = [{'evaluator': evaluator_fullname, 'scores': scores}]

        db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'answers': answers}},
            upsert=True
        )

        return redirect(url_for('user_page'))

    questions_data = db.testText.find()
    questions_list = list(questions_data)

    if questions_list:
        return render_template('test_page.html', questions_list=questions_list)
    else:
        return 'Вопросы не найдены в базе данных.'