# from chatterbot_response import *

# response = debug("hdufhfihdsinfdjgfijh")
# print(response, response.confidence)


import sqlite3

database_file = "database.db"

def get_response(dictionary):
    intent = dictionary['intent']
    subject = dictionary['subject']
    
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute("SELECT %s FROM subjects WHERE subject='%s'" %(intent, subject))
    response = cursor.fetchone()
    if response:
        return response[0]
    else:
        return "দুঃখিত, এব্যাপারে আমার কাছে কোনো তথ্য নেই।"


def record_exists(subject):
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM subjects WHERE subject='%s')" %(subject))
    response = cursor.fetchone()[0]

    return True if response == 1 else False


def debug():
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    cursor.execute("SELECT subject FROM subjects")

    response = cursor.fetchall()
    subjects = [element[0] for  element in response]
    print(subjects)




debug()