from datetime import datetime
import sqlite3


def calculate_overall_average(user_manager, user_id):
    user_answers = user_manager.get_user_answers(user_id)
    scores = [answer[0] for answer in user_answers]

    if len(scores) == 0:
        return "0%"

    total = sum(scores)
    average = (total / len(scores)) * 100
    return str(int(average)) + "%"


def calculate_theme_averages(user_manager, user_id, theme_manager):
    user_answers = user_manager.get_user_answers(user_id)
    theme_ids = theme_manager.get_theme_ids()
    result = []

    for theme_id in theme_ids:
        theme_scores = []
        for answer in user_answers:
            question_theme_id = theme_manager.get_question_theme_id(answer[2])
            if question_theme_id == theme_id[0]:
                theme_scores.append(answer[0])

        if len(theme_scores) == 0:
            result.append("0%")
        else:
            average = (sum(theme_scores) / len(theme_scores)) * 100
            result.append(str(int(average)) + "%")

    return result


def calculate_daily_theme_averages(user_manager, user_id, theme_manager):
    user_answers = user_manager.get_user_answers(user_id)
    theme_ids = theme_manager.get_theme_ids()
    today = datetime.now().strftime("%Y%m%d")
    result = []

    for theme_id in theme_ids:
        theme_scores = []
        for answer in user_answers:
            question_theme_id = theme_manager.get_question_theme_id(answer[2])
            if str(answer[1]) == today and question_theme_id == theme_id[0]:
                theme_scores.append(answer[0])

        if len(theme_scores) == 0:
            result.append("0%")
        else:
            average = (sum(theme_scores) / len(theme_scores)) * 100
            result.append(str(int(average)) + "%")

    return result


def calculate_monthly_theme_averages(user_manager, user_id, theme_manager):
    user_answers = user_manager.get_user_answers(user_id)
    theme_ids = theme_manager.get_theme_ids()
    current_month = datetime.now().strftime("%Y%m")
    result = []

    for theme_id in theme_ids:
        theme_scores = []
        for answer in user_answers:
            question_theme_id = theme_manager.get_question_theme_id(answer[2])
            if str(answer[1])[0:6] == current_month and question_theme_id == theme_id[0]:
                theme_scores.append(answer[0])

        if len(theme_scores) == 0:
            result.append("0%")
        else:
            average = (sum(theme_scores) / len(theme_scores)) * 100
            result.append(str(int(average)) + "%")

    return result


def calculate_yearly_theme_averages(user_manager, user_id, theme_manager):
    user_answers = user_manager.get_user_answers(user_id)
    theme_ids = theme_manager.get_theme_ids()
    current_year = datetime.now().strftime("%Y")
    result = []

    for theme_id in theme_ids:
        theme_scores = []
        for answer in user_answers:
            question_theme_id = theme_manager.get_question_theme_id(answer[2])
            if str(answer[1])[0:4] == current_year and question_theme_id == theme_id[0]:
                theme_scores.append(answer[0])

        if len(theme_scores) == 0:
            result.append("0%")
        else:
            average = (sum(theme_scores) / len(theme_scores)) * 100
            result.append(str(int(average)) + "%")

    return result
