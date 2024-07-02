from bson import ObjectId
from flask import render_template, request, session
from routes.login import users, db

# Assuming testText is a collection in your MongoDB database
testText = db.testText
answersForCompententies = db.answersForCompententies


def user_info(user_id):
    ########### Данные для подписей графиков и подписей осей
    user_id = ObjectId(user_id)
    role = request.args.get('role')

    user = users.find_one({'_id': user_id})

    test_texts = testText.find({}, {'name': 1, 'questions': 1})

    test_texts_list = list(test_texts)
    print(test_texts_list)
    ########### Данные для подписей графиков и подписей осей
    ########### Данные для роли
    role_data = answersForCompententies.find_one({'role': role})

    numerical_data = []
    for item in role_data['names']:
        for value in item.values():
            numerical_data.append(value)
    print(numerical_data)
    ########### Данные для роли
    ########### Средние данные
    answers = user.get('answers', [])
    print(answers)

    # Calculate average scores
    if answers:
        score_sums = {}
        score_counts = {}

        for answer in answers:
            scores = answer['scores']
            for competency, score in scores.items():
                if competency in score_sums:
                    score_sums[competency] += score
                    score_counts[competency] += 1
                else:
                    score_sums[competency] = score
                    score_counts[competency] = 1

        average_scores = {competency: score_sums[competency] / score_counts[competency] for competency in score_sums}
        average_scores_list = list(average_scores.values())
        print(average_scores_list)

        chunked_average_scores = [average_scores_list[i:i + 4] for i in range(0, len(average_scores_list), 4)]
        print(chunked_average_scores)
    else:
        chunked_average_scores = []
    ########### Средние данные
    ########### Данные одного пользователя
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

    print(chunked_scores_data)

    return render_template('user_info.html',
                           user=user, role=role,
                           test_texts=test_texts_list,
                           role_data=numerical_data,
                           average_scores=chunked_average_scores,
                           user_answers=chunked_scores_data)
