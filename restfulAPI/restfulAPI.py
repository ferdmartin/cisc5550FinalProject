#!flask/bin/python
from flask import Flask, request, jsonify
import psycopg2
import urllib

POSTGRESQL_URI = "postgres://nihthtdn:DGu34dLgobeQmcaiKp0yCdbqPHiBxfan@chunee.db.elephantsql.com/nihthtdn"
connection = psycopg2.connect(POSTGRESQL_URI)

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_URI

@app.route("/api/tasks", methods=['GET'])
def show_list():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT what_to_do, due_date, status FROM entries')
            entries = cursor.fetchall()
    if entries != None:
        tdlist = [dict(what_to_do=row[0], due_date=row[1], status=row[2])
                for row in entries]
    else:
        tdlist = []
    return jsonify(tdlist)


@app.route("/api/tasks", methods=['POST'])
def add_entry():
    print(request.json)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("insert into entries values (%s, %s);",
               [request.json['what_to_do'], request.json['due_date']])
    return jsonify({'result':True})


@app.route("/api/tasks/<item>", methods=['DELETE'])
def delete_entry(item):
    item = urllib.parse.unquote(item)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM entries WHERE what_to_do='"+item+"'")
    return jsonify({'result':True})

@app.route("/api/tasks/<item>", methods=['PUT'])
def mark_as_done(item):
    item = urllib.parse.unquote(item)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE entries SET status='done' WHERE what_to_do='"+item+"'")
    return jsonify({'result':True})

if __name__ == "__main__":
    app.run("0.0.0.0", port=5001)