from flask import session, render_template

from routes.login import users
from routes.user_info import answersForCompententies


def team_info():
    current_team = (session.get('team', '')).split(' ')[-1]
    all_users_cursor = users.find({'team': {'$eq': current_team}})
    all_users = list(all_users_cursor)
    comparison_results = []
    success = True

    role_names = []
    for user in all_users:
        distributed_values = user.get('distributed_values', {})
        role_names.extend(distributed_values.keys())

    role_names = list(set(role_names))

    options = [
        "Визионер",
        "Стратегический лидер",
        "Проектный лидер",
        "Проектный аналитик",
        "Предприниматель",
        "Методолог",
        "Коммуникатор",
        "Интегратор",
        "Эксперт",
        "Поставщик ресурсов",
        "Исполнитель",
        "Контролер"
    ]

    for role in role_names:
        if role in options:
            options.remove(role)

    for user in all_users:
        user_comparison = []

        ###### Данные о ответах пользователя
        user_data = user.get('answers', [])
        fullname = user.get('fullname')
        filtered_data = [entry for entry in user_data if entry.get('evaluator') == fullname]

        if filtered_data:
            evaluator_data = filtered_data[0]
            scores = evaluator_data.get('scores', {})
            scores_data = list(scores.values())
            chunked_scores_data = [scores_data[i:i + 4] for i in range(0, len(scores_data), 4)]
        else:
            chunked_scores_data = None
        ###### Данные о ответах пользователя

        ###### Роли пользователя
        distributed_values = user.get('distributed_values', {})
        ###### Роли пользователя

        ###### Нахождение ответов для ролей
        numerical_data = []
        for role in distributed_values:
            role_data = answersForCompententies.find_one({'role': role})

            for item in role_data['names']:
                for value in item.values():
                    numerical_data.append(value)
        ##### Нахождение ответов для ролей

        ##### Сравнение ответов и того как должно быть
        if chunked_scores_data and len(chunked_scores_data) >= len(numerical_data) / 6:
            for i in range(0, len(numerical_data), 6):
                # Сравниваем каждые 6 значений из numerical_data с chunked_scores_data
                comparison_result = numerical_data[i:i + 6] <= chunked_scores_data
                if comparison_result:
                    success = False
                user_comparison.append(comparison_result)

        comparison_results.append(user_comparison)
    return render_template('team_info.html', users=all_users, current_team=current_team, comparison_results=comparison_results, options=options, success=success)
