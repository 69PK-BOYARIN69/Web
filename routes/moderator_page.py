from flask import session, render_template


def moderator_page():
    team = (session.get('team', '')).split(' ')[-1]
    return render_template('moderator_page.html',team=team)