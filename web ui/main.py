from flask import Flask
from flask import request
from flask import render_template
import pymysql.cursors

app = Flask(__name__)


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1133',
                             db='tododb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


users = []


@app.route('/', methods=['GET', 'POST'])
def all_users():
    global connection
    global users
    quests = []
    donequests = []
    with connection.cursor() as cursor:
        for i in range(1, 10):
            sql = "SELECT * FROM user WHERE id=%s"
            cursor.execute(sql, (i))
            try:
                result = cursor.fetchone()
                if result.get('username') is not None and result.get('username') not in users:
                    users.append(result.get('username'))
                elif result.get('id') is None:
                    print('break q')
                    break
            except:
                pass
        for i in range(1, 10):
            sql = "SELECT * FROM `quests` WHERE `done`=%s AND id=%s"
            cursor.execute(sql, (0, i))
            try:
                quest = cursor.fetchone()
                if quest.get('messages') is not None and quest.get('messages') not in quests:
                    quests.append(quest.get('messages'))
                elif quest.get('id') is None:
                    print('break q')
                    break
            except:
                pass
            for i in range(1, 10):
                sql = "SELECT * FROM `quests` WHERE `done`=%s AND id=%s"
                cursor.execute(sql, (1, i))
                try:
                    donequest = cursor.fetchone()
                    if donequest.get('messages') is not None and donequest.get('messages') not in donequests:
                        donequests.append(donequest.get('messages'))
                    elif donequest.get('id') is None:
                        print('break d')
                        break
                except:
                    pass
    if request.method == 'POST':
        try:
            if request.form['done'] != '':
                done = request.form['done']
                welldone = ('%{}%'.format(done))
                print(done)
                with connection.cursor() as cursor:
                    sql = "UPDATE quests SET done=(%s) WHERE messages LIKE  %s "
                    cursor.execute(sql, (1, welldone))
                    print(sql)
                    connection.commit()
                    print('quest done')
        except:
            pass
        try:
            if request.method is not None and request.form['new'] != '':
                new = request.form['new']
                print(new)
                with connection.cursor() as cursor:
                    sql = "INSERT INTO quests (messages,done) VALUES (%s, %s)"
                    cursor.execute(sql, (new, 0))
                    connection.commit()
                    print('done')
        except:
            pass
    print(users, quests, donequests)
    return render_template('user_message.html', users=users, donequests=donequests, quests=quests)


if __name__ == '__main__':
    app.run(debug=True)
