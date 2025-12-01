import random
from question_manager import *
from theme_manager import *


def get_random_question(theme_manager, question_manager):
    themes = theme_manager.get_themes()
    theme_id = int(random.random() * len(themes) + 1)

    questions = question_manager.get_questions_by_theme(theme_id)
    while len(questions) == 0:
        theme_id = int(random.random() * len(themes) + 1)
        questions = question_manager.get_questions_by_theme(theme_id)

    random_index = int(random.random() * len(questions))
    question_id, question, ans1, ans2, ans3, ans4, correct = questions[random_index]

    answers = [ans1, ans2, ans3, ans4]
    random.shuffle(answers)
    ans1, ans2, ans3, ans4 = answers

    return question_id, question, ans1, ans2, ans3, ans4, correct, theme_manager.get_theme_name_by_id(theme_id)


def get_random_group_question(group_id, theme_manager, question_manager, group_manager):
    theme_id = group_manager.get_group_theme_id(group_id)

    if theme_id == 2:
        return generate_math_question()
    else:
        questions = question_manager.get_questions_by_theme(theme_id)
        random_index = int(random.random() * len(questions))
        question_id, question, ans1, ans2, ans3, ans4, correct = questions[random_index]

        answers = [ans1, ans2, ans3, ans4]
        random.shuffle(answers)
        ans1, ans2, ans3, ans4 = answers

        return question, ans1, ans2, ans3, ans4, correct, theme_manager.get_theme_name_by_id(theme_id)


def generate_math_question():
    question_type = int(random.random() * 3)

    if question_type == 0:
        correct_index = int(random.random() * 4)
        answers = ["0", "0", "0", "0"]

        for i in range(4):
            mult1 = int(random.random() * 8 + 2)
            mult2 = int(random.random() * 998 + 2)
            answers[i] = str(mult1 * mult2)
            if i == correct_index:
                correct = answers[i]
                question = str(mult1) + " * " + str(mult2)

    elif question_type == 1:
        correct_index = int(random.random() * 4)
        answers = ["0", "0", "0", "0"]

        for i in range(4):
            sum1 = int(random.random() * 1000 + 9000)
            sum2 = int(random.random() * 1000)
            sub = int(random.random() * 5000)
            answers[i] = str(sum1 + sum2 - sub)
            if i == correct_index:
                correct = answers[i]
                question = str(sum1) + " + " + str(sum2) + " - " + str(sub)

    elif question_type == 2:
        correct_index = int(random.random() * 4)
        answers = ["0", "0", "0", "0"]

        for i in range(4):
            dividend = int(random.random() * 998 + 2)
            divisor = int(random.random() * 8 + 2)
            answers[i] = str(int(dividend / divisor))
            if i == correct_index:
                correct = answers[i]
                question = str(dividend) + "/" + str(divisor)

    return question, correct, answers[0], answers[1], answers[2], answers[3], "Mathematics"
