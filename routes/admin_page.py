from flask import session, render_template

from routes.user_page import user_page


def admin_page():
    return render_template('admin_page.html')