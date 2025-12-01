import sqlite3
from connection_manager import *


class DatabaseSetup:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

        self.drop_theme = "DROP TABLE IF EXISTS theme;"
        self.create_theme = '''
        CREATE TABLE theme(
            id INTEGER,
            name VARCHAR(50),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        '''
        self.load_theme = '''
        INSERT INTO theme VALUES (NULL,"Geography and History"),
        (NULL,"Mathematics"),(NULL,"Language"),(NULL,"Physics and Chemistry")
        '''

        self.drop_user = "DROP TABLE IF EXISTS user;"
        self.create_user = '''
        CREATE TABLE user(
            id INTEGER,
            name VARCHAR(30),
            password VARCHAR(10),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        '''
        self.load_user = '''
        INSERT INTO user VALUES(NULL,"Hugo","1234"),(NULL,"Martin","1234"),
        (NULL,"Paco","1234"),(NULL,"Angel","1234"),(NULL,"Luis","1234")
        '''

        self.drop_answer = "DROP TABLE IF EXISTS answer;"
        self.create_answer = '''
        CREATE TABLE answer(
            id INTEGER,
            user_id INTEGER,
            date DATE,
            question_id INTEGER,
            correct_answer INT,
            FOREIGN KEY (question_id) REFERENCES question(id),
            FOREIGN KEY (user_id) REFERENCES user(id),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        '''

        self.drop_friend = "DROP TABLE IF EXISTS friend;"
        self.create_friend = '''
        CREATE TABLE friend (
            id INTEGER,
            user_id_1 INTEGER,
            user_id_2 INTEGER,
            FOREIGN KEY (user_id_1) REFERENCES user(id),
            FOREIGN KEY (user_id_2) REFERENCES user(id),
            CONSTRAINT fk_user_unique UNIQUE (user_id_1, user_id_2),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        '''

        self.drop_group = "DROP TABLE IF EXISTS \"group\";"
        self.create_group = '''
        CREATE TABLE "group"(
            id INTEGER,
            theme_id INTEGER,
            name VARCHAR(50),
            FOREIGN KEY (theme_id) REFERENCES theme(id),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        '''

        self.drop_user_group = "DROP TABLE IF EXISTS user_group;"
        self.create_user_group = '''
        CREATE TABLE user_group(
            group_id INTEGER,
            user_id INTEGER,
            score INTEGER,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (group_id) REFERENCES "group"(id)
        );
        '''

        self.drop_question = "DROP TABLE IF EXISTS question;"
        self.create_question = '''
        CREATE TABLE question(
            id INTEGER,
            question VARCHAR(50),
            answer_1 VARCHAR(50),
            answer_2 VARCHAR(50),
            answer_3 VARCHAR(50),
            answer_4 VARCHAR(50),
            correct VARCHAR(50),
            theme_id INTEGER,
            FOREIGN KEY (theme_id) REFERENCES theme(id),
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        '''
        self.load_question = '''
        INSERT INTO question VALUES
        (NULL,"What is the capital of Spain?","Madrid","Seville","Barcelona","Valencia","Madrid",1),
        (NULL,"What is the capital of Portugal?","Lisbon","Porto","Aveiro","Lagos","Lisbon",1),
        (NULL,"What is the capital of Germany?","Berlin","Hamburg","Munich","Nuremberg","Berlin",1),
        (NULL,"What is the capital of France?","Paris","Nantes","Normandy","Marseille","Paris",1),
        (NULL,"What is the capital of Poland?","Warsaw","Krakow","Dublin","Wroclaw","Warsaw",1),
        (NULL,"Which continent is Cyprus in?","Europe","Africa","Asia","North America","Europe",1),
        (NULL,"When did Columbus discover America?","1492","1512","1340","1429","1492",1),
        (NULL,"Which country was not part of the Allies in World War II?","Italy","France","Poland","United States","Italy",1),
        (NULL,"How much is 45 divided by 9?","4","5","6","7","5",2),
        (NULL,"How much is 540 divided by 5?","108","120","118","110","108",2),
        (NULL,"How much is 286 divided by 4?","71.5","70","60","64.5","71.5",2),
        (NULL,"How much is 98 divided by 3?","32.6","33","31.3","30","32.6",2),
        (NULL,"How much is 13 multiplied by 9?","117","118","115","116","117",2),
        (NULL,"How much is 62 multiplied by 5?","310","312","319","320","310",2),
        (NULL,"How much is 55 multiplied by 22?","1210","1012","1220","1110","1210",2),
        (NULL,"How much is 428 plus 265 minus 120?","573","602","523","570","573",2),
        (NULL,"How much is 981 plus 258 minus 801?","438","568","439","448","438",2),
        (NULL,"What is the subject of the sentence: I was at the concert with Marta?","SO I","Marta","The","We","SO I",3),
        (NULL,"What is the subject of the sentence: My uncles bought the party gifts?","My uncles","the gifts","I","SO you","My uncles",3),
        (NULL,"What is the subject of the sentence: We don''t know who broke the vase?","SO we","the vase","the","SO they","SO we",3),
        (NULL,"What is the subject of the sentence: The doctor told me to talk to the doctor?","The doctor","the doctor","SO I","me","The doctor",3),
        (NULL,"What class is the following word: with?","Preposition","Adjective","Determiner","Verb","Preposition",3),
        (NULL,"What class is the following word: yellow?","Adjective","Preposition","Verb","Noun","Adjective",3),
        (NULL,"What class is the following word: fly?","Verb","Determiner","Adjective","Noun","Verb",3),
        (NULL,"What does the word tension mean?","State of a body subjected to the action of opposing forces","Property that allows returning to a previous state","Heat released from two colliding objects","Invisible force exerted by a body due to its mass","State of a body subjected to the action of opposing forces",3),
        (NULL,"What is element number 45 on the periodic table?","Rhodium","Sulfur","Gold","Hydrogen","Rhodium",4),
        (NULL,"What is element number 3 on the periodic table?","Lithium","Rhodium","Sodium","Palladium","Lithium",4),
        (NULL,"What is element number 23 on the periodic table?","Vanadium","Copper","Lithium","Oxygen","Vanadium",4),
        (NULL,"What number on the periodic table is Oxygen?","8","24","16","9","8",4),
        (NULL,"What number on the periodic table is Hydrogen?","1","2","12","3","1",4),
        (NULL,"What number on the periodic table is Gold?","79","46","23","34","79",4),
        (NULL,"What number on the periodic table is Platinum?","78","64","70","80","78",4),
        (NULL,"Why do an anvil and a feather fall at the same time on the moon?","Because there is no air resistance","Because objects have no mass in space","Because there is not enough distance","On the moon they don''t fall at the same time","Because there is no air resistance",4)
        '''

    def create_database(self):
        self.cursor.execute(self.drop_theme)
        self.cursor.execute(self.create_theme)
        self.cursor.execute(self.drop_user)
        self.cursor.execute(self.create_user)
        self.cursor.execute(self.drop_answer)
        self.cursor.execute(self.create_answer)
        self.cursor.execute(self.drop_friend)
        self.cursor.execute(self.create_friend)
        self.cursor.execute(self.drop_group)
        self.cursor.execute(self.create_group)
        self.cursor.execute(self.drop_user_group)
        self.cursor.execute(self.create_user_group)
        self.cursor.execute(self.drop_question)
        self.cursor.execute(self.create_question)

    def load_database(self):
        self.cursor.execute(self.load_theme)
        self.cursor.execute(self.load_user)
        self.cursor.execute(self.load_question)
