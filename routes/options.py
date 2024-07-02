import json
from random import random

from bson import ObjectId
from flask import Flask, app, render_template
from flask import Flask, request, redirect, url_for, session, flash

from routes.login import users


def options():
    fullname = session.get('fullname', 'Гость')
    user_data = users.find_one({"fullname": fullname}, {'distributed_values': 1})

    if user_data and 'distributed_values' in user_data:
        distributed_values = user_data['distributed_values']
        user_competencies = list(distributed_values.keys())
    else:
        user_competencies = []

    if request.method == 'POST':
        selected_options = request.form.getlist('option')
        options_str = ','.join(selected_options)
        return redirect(url_for('distribute', options=options_str))

    return render_template('options.html', user_competencies=user_competencies)