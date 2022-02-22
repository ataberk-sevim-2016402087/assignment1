from flask import Flask, request, Response, g
import logging
import sqlite3

# select database
DATABASE = './database.db'

app = Flask(__name__)

## CREATE A NEW TASK

@app.route('/v1/tasks', methods=["POST"])
def save_def():
    if request.headers['Content-Type'] == 'application/json':

        arguments = request.get_json()
        title = arguments.get("title")
        is_completed = arguments.get("is_completed")
        db = get_db()
        if(is_completed == None):
            query = "INSERT INTO tasks_3037426989 (title) VALUES (?)"
            cur = db.execute(query, [title])
            db.commit()
            query = "SELECT MAX(task_id) FROM tasks_3037426989"
            cur = db.execute(query)
            task_id = cur.fetchall()
            logging.warning("title {} saved with {}".format(title,task_id))
        else:
            query = "INSERT INTO tasks_3037426989 (title,is_completed) VALUES (?,?)"
            cur = db.execute(query, [title,is_completed])
            db.commit()
            query = "SELECT MAX(task_id) FROM tasks_3037426989"
            cur = db.execute(query)
            task_id = cur.fetchall()
            cur.close()
            logging.warning("title {} , completed {} saved".format(title,is_completed))
    else:
            logging.warning("Invalid content type: only application/json is allowed")

    return {"id":task_id[0][0]}


## GET ALL TASKS

@app.route('/v1/tasks', methods=["GET"])
def get_all():



    db = get_db()
    query = "SELECT * from tasks_3037426989"
    cur = db.execute(query)
    rv = cur.fetchall()
    cur.close()
    tasklist = list()
    for tasks in list(rv):
            tasklist.append({
                'task_id': tasks[0],
                'title': tasks[1],
                'is_completed': tasks[2],
            })

    if(len(tasklist)==0):
        return "None"
    else:
        return {'tasks': tasklist}

## GET A SPECIFIC TEST

@app.route('/v1/tasks/<id>', methods=["GET"])
def get_spec(id):
    db = get_db()
    try:
        query = "SELECT * FROM tasks_3037426989 WHERE task_id = ? "
        cur = db.execute(query , [id])
        result = cur.fetchall()
        cur.close()
        return {"id": result[0][0], "title": result[0][1], "is_completed": result[0][2]}
    except:
        return Response(""),404


## DELETE A SPECIFIC TEST

@app.route('/v1/tasks/<id>', methods=["DELETE"])
def del_tasks(id):
    db = get_db()
    query = "SELECT * FROM tasks_3037426989 WHERE task_id=? "
    cur = db.execute(query, [id])
    result = cur.fetchall()
    if(len(result)==0):
        return Response(""),404
    else:
        query = "DELETE FROM tasks_3037426989 WHERE task_id = ?"
        cur = db.execute(query, [id])
        db.commit()
        cur.close()
        return Response("")

## EDIT a TASK

@app.route('/v1/tasks/<id>', methods=["PUT"])
def edit_tasks(id):
    if request.headers['Content-Type'] == 'application/json':

        arguments = request.get_json()
        title = arguments.get("title")
        is_completed = arguments.get("is_completed")
        db = get_db()
        query = "SELECT * FROM tasks_3037426989 WHERE task_id=? "
        cur = db.execute(query, [id])
        result = cur.fetchall()
        if (len(result) == 0):
            return Response(""), 404
        if(is_completed == None):
            query = "UPDATE tasks_3037426989 SET title = (?) WHERE task_id = (?) "
            cur = db.execute(query, [title,id])
            db.commit()
            cur.close()
        else:
            query = "UPDATE tasks_3037426989 SET title = (?), is_completed= (?) WHERE task_id = (?)"
            cur = db.execute(query, [title,is_completed,id])
            db.commit()
            cur.close()
    else:
            logging.warning("Invalid content type: only application/json is allowed")

    return Response("")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        schema_sql = """
          CREATE TABLE IF NOT EXISTS tasks_3037426989 (
            task_id  INTEGER PRIMARY KEY,
            title  VARCHAR(50) NOT NULL,
            is_completed  BOOLEAN NOT NULL DEFAULT FALSE
          );
        """
        cur = db.execute(schema_sql)
        db.commit()
        cur.close()


if __name__ == "__main__":
  init_db()
  logging.warning("Table created or already exists")
  app.run(host="localhost", port=8000, debug=True)