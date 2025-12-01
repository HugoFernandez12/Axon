import threading
import sys
import os
from datetime import datetime
from flask import render_template, request, Flask, redirect, url_for

from logger import *
from statistics import *
from question_generator import *
from database_setup import *
from connection_manager import *
from database_lister import *
from friend_manager import *
from group_manager import *
from question_manager import *
from theme_manager import *
from user_manager import *

log = Logger(22999, 10, 7)

if not os.path.exists('database'):
    os.makedirs('database')

connection, cursor = get_cursor()

db_setup = DatabaseSetup(connection, cursor)

try:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
    if cursor.fetchone() is None:
        db_setup.create_database()
        db_setup.load_database()
        connection.commit()
except:
    db_setup.create_database()
    db_setup.load_database()
    connection.commit()

db_lister = DatabaseLister(connection, cursor)
theme_manager = ThemeManager(connection, cursor)
friend_manager = FriendManager(connection, cursor)
group_manager = GroupManager(connection, cursor)
question_manager = QuestionManager(connection, cursor)
user_manager = UserManager(connection, cursor)

current_user = ""
question_count = 0
user_correct_answers = [0, 0, 0, 0, 0]
temp_correct_answer = ""
error_message = ""
group_friends = []
group_name = ""
selected_group_id = 0
admin_group_id = 0
control_message = ""
profile_user = ""
selected_question_id = 0
filter_theme_control = 0
question_ids = []
questions_list = []
group_theme = ""
filter_theme = ""
modify_question_control = True
user_controls = []

app = Flask(__name__)


@app.route('/main', methods=['GET', 'POST'])
def main():
    global current_user
    if current_user == "":
        return redirect("/")

    return render_template('main.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    global current_user
    if current_user == "":
        return redirect("/")

    log.information(f"User {current_user} is viewing their profile.")

    data = request.form
    period = "Day"

    user_id = user_manager.get_user_id_by_name(current_user)
    overall_average = calculate_overall_average(user_manager, user_id)
    themes = theme_manager.get_themes()
    themes_count = len(themes)

    daily_averages = calculate_daily_theme_averages(user_manager, user_id, theme_manager)
    monthly_averages = calculate_monthly_theme_averages(user_manager, user_id, theme_manager)
    yearly_averages = calculate_yearly_theme_averages(user_manager, user_id, theme_manager)
    overall_averages = calculate_theme_averages(user_manager, user_id, theme_manager)

    if len(data) != 0:
        if request.form.get("friends") == "Friends":
            log.information(f"User {current_user} accessed friends manager.")
            return redirect("/friends")
        if request.form.get("groups") == "Groups":
            log.information(f"User {current_user} accessed groups management.")
            return redirect("/groups")
        if request.form.get("change_password") == "Change Password":
            log.information(f"User {current_user} accessed password management.")
            return redirect("/change-password")
        if request.form.get("logout") == "Logout":
            log.information(f"User {current_user} logged out.")
            return redirect("/")

        period = request.form.get("period")

    return render_template('profile.html', current_user=current_user, period=period,
                           themes=themes, themes_count=themes_count,
                           overall_average=overall_average, daily_averages=daily_averages,
                           monthly_averages=monthly_averages, yearly_averages=yearly_averages,
                           overall_averages=overall_averages)


@app.route('/friends', methods=['GET', 'POST'])
def friends():
    global current_user, error_message
    if current_user == "":
        return redirect("/")

    error_message = ""
    data = request.form

    user_id = user_manager.get_user_id_by_name(current_user)
    friends_list = friend_manager.get_friends(user_id)
    friends_count = len(friends_list)

    if len(data) != 0:
        if request.form.get("add_friend") == "Add":
            friend_name = request.form.get("friend_name")
            if friend_name != "":
                try:
                    friend_id = user_manager.get_user_id_by_name(friend_name)
                    friend_manager.add_friend(user_id, friend_id)
                    connection.commit()
                    log.information(f"User {current_user} added a new friend.")
                    return redirect("/friends")
                except:
                    error_message = f"User {friend_name} not found or already added."
                    log.error(f"ERROR: User {friend_name} not found or already added.")
            else:
                error_message = "Name cannot be empty"
                log.error("ERROR: Friend name is empty.")

    friend_scores = []
    for friend in friends_list:
        friend_scores.append(calculate_overall_average(user_manager, user_manager.get_user_id_by_name(friend[0])))

    return render_template('friends.html', friends_list=friends_list, error_message=error_message,
                           friends_count=friends_count, friend_scores=friend_scores)


@app.route('/play', methods=['GET', 'POST'])
def play():
    global question_count, temp_correct_answer, current_user, user_correct_answers
    correct_answers_count = len(user_correct_answers)

    if current_user == "":
        return redirect("/")

    data = request.form
    if len(data) != 0 and not request.form.get("play") and request.form.get("question_id"):
        question_id = int(request.form.get("question_id"))

        if request.form.get("exit_game") == "1":
            user_manager.save_answer(user_manager.get_user_id_by_name(current_user), question_id, 0)
            connection.commit()
            log.information(f"User {current_user} exited game, question marked as incorrect.")
            user_correct_answers[question_count] = 0
            question_count = question_count + 1
        elif request.form.get("answer1") == temp_correct_answer or request.form.get("answer2") == temp_correct_answer or \
                request.form.get("answer3") == temp_correct_answer or request.form.get(
            "answer4") == temp_correct_answer:
            user_manager.save_answer(user_manager.get_user_id_by_name(current_user), question_id, 1)
            connection.commit()
            log.information(f"User {current_user} answered correctly.")
            user_correct_answers[question_count] = 1
            question_count = question_count + 1
        else:
            user_manager.save_answer(user_manager.get_user_id_by_name(current_user), question_id, 0)
            connection.commit()
            log.information(f"User {current_user} answered incorrectly")
            user_correct_answers[question_count] = 0
            question_count = question_count + 1

    log.information(f"User {current_user} is playing.")

    question_id, question_text, answer1, answer2, answer3, answer4, correct, theme = get_random_question(theme_manager,
                                                                                                         question_manager)

    temp_correct_answer = correct

    return render_template('play.html', theme=theme, question_text=question_text, correct=correct,
                           answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4,
                           user_correct_answers=user_correct_answers, question_count=question_count,
                           correct_answers_count=correct_answers_count, question_id=question_id)


@app.route('/play-group', methods=['GET', 'POST'])
def play_group():
    global temp_correct_answer, current_user
    if current_user == "":
        return redirect("/")

    group_name_display = group_manager.get_group_name(selected_group_id)
    log.information(f"User {current_user} is playing in group {group_name_display}.")

    question_text, answer1, answer2, answer3, answer4, correct, theme = get_random_group_question(
        selected_group_id, theme_manager, question_manager, group_manager
    )

    data = request.form
    if len(data) != 0:
        if request.form.get("answer1") == temp_correct_answer or request.form.get("answer2") == temp_correct_answer or \
                request.form.get("answer3") == temp_correct_answer or request.form.get(
            "answer4") == temp_correct_answer:
            group_manager.increment_score(selected_group_id, user_manager.get_user_id_by_name(current_user))
            connection.commit()
            log.information(f"User {current_user} answered correctly in group {group_name_display}.")

    temp_correct_answer = correct

    return render_template('play_group.html', question_text=question_text, correct=correct,
                           answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4,
                           group_name_display=group_name_display)


@app.route('/', methods=['GET', 'POST'])
def index():
    global error_message, current_user, question_count, user_correct_answers
    question_count = 0
    current_user = ""
    error_message = ""

    data = request.form
    if len(data) != 0:
        username = request.form.get("username")
        username = username.strip()
        password = request.form.get("password")
        password = password.strip()
        login = request.form.get("login")
        register = request.form.get("register")

        if login == "Login":
            if username == "admin" and password == "admin":
                current_user = username
                log.information(f"User {current_user} logged in.")
                log.information(f"User {current_user} accessed questions manager.")
                user_correct_answers = [0, 0, 0, 0, 0]
                return redirect("/admin-groups")

            try:
                user_id = user_manager.get_user_id_by_name(username)
                user_password = user_manager.get_password(username)
                if password == user_password:
                    current_user = username

                    today = datetime.now().strftime("%Y%m%d")
                    cursor.execute(
                        "SELECT correct_answer FROM answer WHERE user_id=(?) AND date=(?)",
                        (user_id, today)
                    )
                    today_answers = cursor.fetchall()
                    question_count = len(today_answers)

                    user_correct_answers = [0, 0, 0, 0, 0]
                    for i, answer in enumerate(today_answers):
                        if i < 5:
                            user_correct_answers[i] = answer[0]

                    log.information(f"User {current_user} logged in.")
                    log.information(f"User {current_user} accessed main menu.")
                    return redirect("/main")
                else:
                    error_message = "Incorrect password"
                    log.error("ERROR: Password not found.")
            except:
                error_message = "User not found"
                log.error("ERROR: User not found.")

        elif register == "Register":
            try:
                user_id = user_manager.get_user_id_by_name(username)
                error_message = "User already exists"
                log.error("ERROR: User already exists.")
            except:
                if username != "" and password != "":
                    user_manager.create_user(username, password)
                    connection.commit()
                    current_user = username
                    question_count = 0
                    user_correct_answers = [0, 0, 0, 0, 0]
                    log.information(f"User {current_user} registered in Axon.")
                    log.information(f"User {current_user} accessed main menu.")
                    return redirect("/main")
                else:
                    error_message = "Username and password cannot be empty"
                    log.error("ERROR: Username or password cannot be empty.")

    return render_template('login.html', error_message=error_message)


@app.route('/groups', methods=['GET', 'POST'])
def groups():
    global current_user, selected_group_id, group_friends
    if current_user == "":
        return redirect("/")

    user_id = user_manager.get_user_id_by_name(current_user)

    groups_list = []
    scores_list = []

    groups_scores = group_manager.get_user_groups_scores(user_id)
    groups_scores_count = len(groups_scores)

    for i in range(0, groups_scores_count):
        groups_list.append(group_manager.get_group_name(groups_scores[i][0]))
        scores_list.append(groups_scores[i][1])

    data = request.form
    if len(data) != 0:
        if request.form.get("create_group") == "Create Group":
            log.information(f"User {current_user} accessed group creation.")
            user_controls.clear()
            group_friends.clear()
            return redirect("/create-group")

        for i in range(0, groups_scores_count):
            if "Play" == request.form.get(str(i)):
                selected_group_id = groups_scores[i][0]
                return redirect("/play-group")

        for i in range(0, groups_scores_count):
            if "View Group" == request.form.get(str(i)):
                selected_group_id = groups_scores[i][0]
                return redirect("/view-group")

        for i in range(0, groups_scores_count):
            if "Leave Group" == request.form.get(str(i)):
                group_to_delete = groups_scores[i][0]
                group_manager.remove_user_from_group(group_to_delete, user_id)
                connection.commit()
                return redirect("/groups")

    return render_template('groups.html', groups_list=groups_list, scores_list=scores_list,
                           groups_scores_count=groups_scores_count)


@app.route('/create-group', methods=['GET', 'POST'])
def create_group():
    global current_user, group_friends, error_message, group_name, control_message, group_theme, user_controls

    if current_user == "":
        return redirect("/")

    control_message = ""
    error_message = ""
    proceed = True
    group_exists = False
    has_users = False

    user_id = user_manager.get_user_id_by_name(current_user)
    friends_list = friend_manager.get_friends(user_id)
    friends_count = len(friends_list)
    themes = theme_manager.get_themes()

    if len(user_controls) == 0:
        for i in range(0, friends_count):
            user_controls.append(0)

    user_controls_count = len(user_controls)
    group_friends_count = len(group_friends)

    data = request.form
    if len(data) != 0:
        group_name = request.form.get("group_name")
        group_name = group_name.strip()

        for i in range(0, friends_count):
            if "Add" == request.form.get(str(i)):
                user_controls[i] = 1
                group_theme = request.form.get("theme")

                for j in range(0, group_friends_count):
                    if friends_list[i] == group_friends[j]:
                        proceed = False
                        break

                if proceed:
                    group_friends.append(friends_list[i])
                    group_friends_count = len(group_friends)
                else:
                    break

        if request.form.get("clear_friends") == "Clear All":
            user_controls.clear()
            for i in range(0, friends_count):
                user_controls.append(0)
            user_controls_count = len(user_controls)
            group_theme = request.form.get("theme")
            group_friends.clear()
            group_friends_count = len(group_friends)

        if request.form.get("create_group") == "Create Group":
            try:
                group_theme = request.form.get("theme")
                theme_id = theme_manager.get_theme_id_by_name(group_theme)
                user_ids_array = []

                for i in range(0, group_friends_count):
                    friend_id = user_manager.get_user_id_by_name(group_friends[i][0])
                    user_ids_array.append(friend_id)

                if len(user_ids_array) != 0:
                    has_users = True
                    user_ids_array.append(user_id)

                for i in range(0, len(group_manager.get_groups())):
                    if group_manager.get_groups()[i][0] == group_name:
                        group_exists = True
                        break

                if not group_exists:
                    if has_users:
                        if group_name != "":
                            group_manager.create_group(theme_id, group_name, user_ids_array)
                            connection.commit()
                            control_message = "Group created successfully"
                            log.information(f"User {current_user} created group {group_name}.")
                            group_name = ""
                        else:
                            error_message = "Group name cannot be empty"
                            log.error("ERROR: Group name cannot be empty.")
                    else:
                        error_message = f"No users were added to group {group_name}"
                        log.error("ERROR: No users assigned to group.")
                else:
                    error_message = "Group already exists"
                    log.error("ERROR: Could not create group.")
            except:
                error_message = "Error creating group"
                log.error("ERROR: Could not create group.")

    return render_template('create_group.html', control_message=control_message, group_name=group_name,
                           error_message=error_message, friends_list=friends_list, friends_count=friends_count,
                           group_friends=group_friends, group_friends_count=group_friends_count,
                           themes=themes, group_theme=group_theme, user_controls=user_controls)


@app.route('/admin-create-question', methods=['GET', 'POST'])
def admin_create_question():
    global current_user, error_message, control_message
    if current_user != "admin":
        return redirect("/")

    error_message = ""
    control_message = ""

    themes = theme_manager.get_themes()
    data = request.form

    if len(data) != 0:
        if request.form.get("logout") == "Logout":
            log.information("Admin logged out.")
            return redirect("/")

        if request.form.get("create_question") == "Create Question":
            question_text = request.form.get("question")
            answer1 = request.form.get("answer1")
            answer2 = request.form.get("answer2")
            answer3 = request.form.get("answer3")
            answer4 = request.form.get("answer4")
            theme = request.form.get("theme")

            try:
                if question_text != "" and answer1 != "" and answer2 != "" and answer3 != "" and answer4 != "":
                    question_manager.create_question(question_text, answer1, answer2, answer3, answer4,
                                                     theme_manager.get_theme_id_by_name(theme))
                    connection.commit()
                    log.information(f"User {current_user} created a new question.")
                    control_message = "Question created successfully"
                else:
                    error_message = "Fields cannot be empty"
                    log.error("ERROR: Question fields are empty.")
            except:
                error_message = "Error creating question"
                log.error("ERROR: Could not create question.")

    return render_template('admin_create_question.html', error_message=error_message,
                           control_message=control_message, themes=themes)


@app.route('/view-group', methods=['GET', 'POST'])
def view_group():
    global current_user, error_message, selected_group_id
    if current_user == "":
        return redirect("/")

    error_message = ""

    try:
        users_list = []
        scores_list = []
        group_name_display = group_manager.get_group_name(selected_group_id)
        group_id = selected_group_id

        users_scores = group_manager.get_group_users_scores(group_id)
        users_scores_count = len(users_scores)

        for i in range(0, users_scores_count):
            users_list.append(user_manager.get_username(users_scores[i][0]))
            scores_list.append(users_scores[i][1])
    except:
        error_message = "Group does not exist"
        log.error("ERROR: Group does not exist.")

    return render_template('view_group.html', users_scores_count=users_scores_count,
                           group_name_display=group_name_display, users_list=users_list,
                           scores_list=scores_list)


@app.route('/admin-groups', methods=['GET', 'POST'])
def admin_groups():
    global current_user, selected_group_id, error_message
    if current_user != "admin":
        return redirect("/")

    error_message = ""

    groups_list = group_manager.get_groups()
    groups_count = len(groups_list)

    data = request.form
    if len(data) != 0:
        if request.form.get("logout") == "Logout":
            log.information("Admin logged out.")
            return redirect("/")

        for i in range(0, groups_count):
            if "Delete Group" == request.form.get(str(i)):
                group_to_delete = groups_list[i][0]
                group_id_to_delete = group_manager.get_group_id_by_name(group_to_delete)

                group_users = group_manager.get_group_users(group_id_to_delete)
                try:
                    for user in group_users:
                        group_manager.remove_user_from_group(group_id_to_delete, user[0])
                    group_manager.delete_group(group_id_to_delete)
                    connection.commit()
                    return redirect("/admin-groups")
                except:
                    error_message = "Error deleting group"
                    log.error("ERROR: Could not create question.")

        for i in range(0, groups_count):
            if "View Group" == request.form.get(str(i)):
                selected_group_id = groups_list[i][0]
                return redirect("/admin-view-group")

    return render_template('admin_groups.html', groups_count=groups_count, groups_list=groups_list)


@app.route('/admin-users', methods=['GET', 'POST'])
def admin_users():
    global current_user, error_message, profile_user
    if current_user != "admin":
        return redirect("/")

    error_message = ""

    users_list = user_manager.get_users()
    users_count = len(users_list)

    data = request.form
    if len(data) != 0:
        if request.form.get("logout") == "Logout":
            log.information("Admin logged out.")
            return redirect("/")

        for i in range(0, users_count):
            if "View Profile" == request.form.get(str(i)):
                profile_user = users_list[i][0]
                return redirect("/admin-profile")

    return render_template('admin_users.html', error_message=error_message,
                           users_count=users_count, users_list=users_list)


@app.route('/admin-questions', methods=['GET', 'POST'])
def admin_questions():
    global current_user, error_message, control_message, selected_question_id, filter_theme_control
    global question_ids, questions_list, filter_theme, modify_question_control

    if current_user != "admin":
        return redirect("/")

    error_message = ""
    control_message = ""
    selected_question_id = 0

    themes = theme_manager.get_themes()
    all_questions = question_manager.get_questions_with_themes()
    all_questions_count = len(all_questions)

    if modify_question_control:
        if len(questions_list) == 0:
            for i in range(0, all_questions_count):
                question_ids.append(all_questions[i][0])
                questions_list.append(all_questions[i][1])
        questions_count = len(questions_list)
    else:
        questions_list.clear()
        question_ids.clear()
        for i in range(0, all_questions_count):
            question_ids.append(all_questions[i][0])
            questions_list.append(all_questions[i][1])
        questions_count = len(questions_list)

    theme_ids = []
    for i in range(0, all_questions_count):
        theme_ids.append(all_questions[i][2])

    data = request.form
    if len(data) != 0:
        if request.form.get("clear_filter") == "Clear Filter":
            modify_question_control = True
            filter_theme_control = 0
            questions_list.clear()
            question_ids.clear()
            return redirect("/admin-questions")

        if request.form.get("filter") == "Filter":
            modify_question_control = True
            filter_theme = request.form.get("theme")
            if filter_theme != "":
                questions_list.clear()
                question_ids.clear()
                for i in range(0, all_questions_count):
                    if theme_manager.get_theme_id_by_name(filter_theme) == theme_ids[i]:
                        filter_theme_control = theme_manager.get_theme_id_by_name(filter_theme)
                        question_ids.append(all_questions[i][0])
                        questions_list.append(all_questions[i][1])
                questions_count = len(questions_list)

        if request.form.get("logout") == "Logout":
            log.information("Admin logged out.")
            return redirect("/")

        for i in range(0, all_questions_count):
            if request.form.get(str(i)) == "Modify Question":
                filter_theme = request.form.get("theme")
                selected_question_id = question_ids[i]
                return redirect("/admin-edit-question")

    return render_template('admin_questions.html', error_message=error_message,
                           control_message=control_message, questions_list=questions_list,
                           questions_count=questions_count, themes=themes, filter_theme=filter_theme)


@app.route('/admin-view-group', methods=['GET', 'POST'])
def admin_view_group():
    global current_user, error_message, selected_group_id, control_message
    if current_user != "admin":
        return redirect("/")

    control_message = ""
    error_message = ""

    try:
        users_list = []
        scores_list = []
        group_name_display = selected_group_id
        group_id = group_manager.get_group_id_by_name(selected_group_id)
        users_scores = group_manager.get_group_users_scores(group_id)

        users_scores_count = len(users_scores)
        for i in range(0, users_scores_count):
            users_list.append(user_manager.get_username(users_scores[i][0]))
            scores_list.append(users_scores[i][1])
    except:
        error_message = "Group does not exist"
        log.error("ERROR: Group does not exist.")

    data = request.form
    if len(data) != 0:
        if request.form.get("logout") == "Logout":
            log.information("Admin logged out.")
            return redirect("/")

        if request.form.get("change_name") == "Change Name":
            new_group_name = request.form.get("new_group_name")
            try:
                if new_group_name != "":
                    if new_group_name != group_name_display:
                        group_exists = False

                        for i in range(0, len(group_manager.get_groups())):
                            if group_manager.get_groups()[i][0] == new_group_name:
                                group_exists = True
                                break

                        if not group_exists:
                            group_manager.update_group_name(group_name_display, new_group_name)
                            connection.commit()
                            log.information("Group name changed successfully.")
                            control_message = "Group name changed successfully"
                            selected_group_id = new_group_name
                            return redirect("/admin-view-group")
                        else:
                            error_message = "A group with that name already exists"
                            log.error("ERROR: A group with that name already exists.")
                else:
                    error_message = "Cannot change name to empty value"
                    log.error("ERROR: Cannot change name to empty value.")
            except:
                error_message = "Could not change group name"
                log.error("ERROR: Could not change group name.")

    return render_template('admin_view_group.html', users_scores_count=users_scores_count,
                           group_name_display=group_name_display, users_list=users_list,
                           scores_list=scores_list, error_message=error_message,
                           control_message=control_message)


@app.route('/admin-profile', methods=['GET', 'POST'])
def admin_profile():
    global current_user, profile_user
    if current_user != "admin":
        return redirect("/")

    log.information(f"Admin is viewing profile of {profile_user}.")

    data = request.form
    period = "Day"

    user_id = user_manager.get_user_id_by_name(profile_user)
    overall_average = calculate_overall_average(user_manager, user_id)

    themes = theme_manager.get_themes()
    themes_count = len(themes)

    daily_averages = calculate_daily_theme_averages(user_manager, user_id, theme_manager)
    monthly_averages = calculate_monthly_theme_averages(user_manager, user_id, theme_manager)
    yearly_averages = calculate_yearly_theme_averages(user_manager, user_id, theme_manager)
    overall_averages = calculate_theme_averages(user_manager, user_id, theme_manager)

    if len(data) != 0:
        if request.form.get("logout") == "Logout":
            log.information("Admin logged out.")
            return redirect("/")

        period = request.form.get("period")

    return render_template('admin_profile.html', profile_user=profile_user, period=period,
                           themes=themes, themes_count=themes_count, overall_average=overall_average,
                           daily_averages=daily_averages, monthly_averages=monthly_averages,
                           yearly_averages=yearly_averages, overall_averages=overall_averages)


@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    global current_user, profile_user, error_message
    if current_user == "":
        return redirect("/")

    control_message = ""
    error_message = ""
    data = request.form

    if len(data) != 0:
        if request.form.get("change_password") == "Change Password":
            old_password = request.form.get("old_password")
            new_password = request.form.get("new_password")

            try:
                current_password = user_manager.get_password(current_user)

                if current_password == old_password:
                    if new_password != "":
                        user_manager.update_password(current_user, new_password)
                        connection.commit()
                        control_message = "Password changed successfully"
                        log.information(f"User {current_user} changed their password.")
                    else:
                        error_message = "Password cannot be empty"
                        log.error(f"ERROR: Password entered by {current_user} is empty.")
                else:
                    error_message = "Current password is incorrect"
                    log.error(f"ERROR: Current password entered by {current_user} is incorrect.")
            except:
                error_message = "Could not change password"
                log.error("ERROR: Could not change password")

    return render_template('change_password.html', error_message=error_message,
                           control_message=control_message)


@app.route('/admin-themes', methods=['GET', 'POST'])
def admin_themes():
    global current_user, error_message, control_message
    if current_user != "admin":
        return redirect("/")

    log.information("Admin is adding themes.")

    control_message = ""
    error_message = ""
    theme_exists = False
    theme_empty = False
    data = request.form

    if len(data) != 0:
        if request.form.get("logout") == "Logout":
            log.information("Admin logged out.")
            return redirect("/")

        if request.form.get("add_theme") == "Add Theme":
            try:
                new_theme = request.form.get("new_theme")
                if new_theme == "":
                    theme_empty = True
                    error_message = "Theme cannot be empty"
                    log.error("ERROR: Theme cannot be empty.")

                themes = theme_manager.get_themes()
                for theme in themes:
                    if new_theme == theme[0]:
                        theme_exists = True

                if theme_exists:
                    error_message = "Theme already exists"
                    log.error("ERROR: Theme already exists.")
                else:
                    if not theme_empty:
                        theme_manager.add_theme(new_theme)
                        connection.commit()
                        control_message = "Theme added successfully"
                        log.information("Admin added a new theme successfully.")
            except:
                error_message = "Could not change password"
                log.error("ERROR: Could not change password")

    return render_template('admin_themes.html', error_message=error_message,
                           control_message=control_message)


@app.route('/admin-edit-question', methods=['GET', 'POST'])
def admin_edit_question():
    global current_user, error_message, control_message, selected_question_id
    global filter_theme_control, modify_question_control

    if current_user != "admin":
        return redirect("/")

    error_message = ""
    control_message = ""
    filter_theme_control = 0

    question_text, answer1, answer2, answer3, answer4, correct, theme_id = question_manager.get_question_by_id(
        selected_question_id)
    theme_name = theme_manager.get_theme_name_by_id(theme_id)
    themes = theme_manager.get_themes()

    data = request.form
    if len(data) != 0:
        if request.form.get("logout") == "Logout":
            log.information("Admin logged out.")
            return redirect("/")

        if request.form.get("modify_question") == "Modify Question":
            new_question = request.form.get("question")
            new_answer1 = request.form.get("answer1")
            new_answer2 = request.form.get("answer2")
            new_answer3 = request.form.get("answer3")
            new_answer4 = request.form.get("answer4")
            new_correct = request.form.get("correct")
            new_theme = request.form.get("theme")

            if new_question == "":
                new_question = question_text
            if new_answer1 == "":
                new_answer1 = answer1
            if new_answer2 == "":
                new_answer2 = answer2
            if new_answer3 == "":
                new_answer3 = answer3
            if new_answer4 == "":
                new_answer4 = answer4
            if new_correct == "":
                new_correct = correct

            try:
                question_manager.update_question(new_question, new_answer1, new_answer2, new_answer3,
                                                 new_answer4, new_correct,
                                                 theme_manager.get_theme_id_by_name(new_theme),
                                                 selected_question_id)
                connection.commit()
                log.information("Admin modified a question.")
                control_message = "Question modified successfully"
                modify_question_control = False
            except:
                error_message = "Error modifying question"
                log.error("ERROR: Could not modify question.")

    return render_template('admin_edit_question.html', error_message=error_message,
                           control_message=control_message, themes=themes, question_text=question_text,
                           answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4,
                           correct=correct, theme_name=theme_name)


def run_server():
    app.run()


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()