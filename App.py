import json
from random import random

from bson import ObjectId
from flask import Flask

from routes.add_user import add_user
from routes.distribute import distribute
from routes.evaluate_user import evaluate_user

from routes.admin_page import admin_page
from routes.delete_user import delete_user
from routes.login import login
from routes.moderator_page import moderator_page
from routes.options import options
from routes.rate_users import rate_users
from routes.team_info import team_info
from routes.test_page import test_page
from routes.user_info import user_info
from routes.user_page import user_page

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.route('/', methods=['GET', 'POST'])(login)
app.route('/user')(user_page)
app.route('/rate_users', methods=['GET'])(rate_users)
app.route('/evaluate_user/<user_id>', methods=['GET', 'POST'])(evaluate_user)
app.route('/test/<user_id>', methods=['GET', 'POST'])(test_page)
app.route('/options', methods=['GET', 'POST'])(options)
app.route('/distribute', methods=['GET', 'POST'])(distribute)
app.route('/admin')(admin_page)
app.route('/admin/add_user', methods=['GET', 'POST'])(add_user)
app.route('/admin/delete_user', methods=['GET', 'POST'])(delete_user)
app.route('/moderator')(moderator_page)
app.route('/moderator/team_info', methods=['GET'])(team_info)
app.route('/moderator/team_info/<user_id>', methods = ['GET'])(user_info)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
