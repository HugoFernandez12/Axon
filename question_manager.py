import sqlite3
from connection_manager import *


class QuestionManager:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def get_questions_with_themes(self):
        self.cursor.execute("SELECT id, question, theme_id FROM question")
        return self.cursor.fetchall()

    def get_question_by_id(self, question_id):
        self.cursor.execute(
            "SELECT question, answer_1, answer_2, answer_3, answer_4, correct, theme_id FROM question WHERE id=(?)",
            (question_id,)
        )
        return self.cursor.fetchall()[0]

    def get_questions_by_theme(self, theme_id):
        self.cursor.execute(
            "SELECT id, question, answer_1, answer_2, answer_3, answer_4, correct FROM question WHERE theme_id=(?)",
            (theme_id,)
        )
        return self.cursor.fetchall()

    def create_question(self, question, answer_1, answer_2, answer_3, answer_4, theme_id):
        self.cursor.execute(
            "INSERT INTO question VALUES(NULL,?,?,?,?,?,?,?)",
            (question, answer_1, answer_2, answer_3, answer_4, answer_1, theme_id)
        )

    def update_question(self, question, answer_1, answer_2, answer_3, answer_4, correct, theme_id, question_id):
        self.cursor.execute(
            "UPDATE question SET question=(?), answer_1=(?), answer_2=(?), answer_3=(?), answer_4=(?), correct=(?), theme_id=(?) WHERE id=(?)",
            (question, answer_1, answer_2, answer_3, answer_4, correct, theme_id, question_id)
        )
