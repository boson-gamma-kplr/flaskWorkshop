import flask

from flask import request, Flask, jsonify, render_template, redirect, url_for
import json
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
       

def connect():
    try:
        conn = psycopg2.connect(
                user = "igudfqsi",
                password = "7SMOHysbUXXIU9yc0dFKVFM0TW5zTQQr",
                host = "horton.db.elephantsql.com",
                port = "5432",
                database = "igudfqsi"
            )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # cur = conn.cursor()
        print("La connexion PostgreSQL est ouverte")
        return [conn, cur]
    except (Exception, psycopg2.Error) as error :
        print ("Erreur lors de la connexion à PostgreSQL", error)
        return [None,None]
    
def version():
    conn, cur = connect()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("Version : ", version,"\n")
    cur.close()
    conn.close()

@app.route("/", methods=["POST", "GET"])
def home_page():
    if request.method == "POST":
        if 'view_all' in request.form:
            return redirect(url_for("get_all_data"))
        elif 'view_one' in request.form:
            return redirect(url_for('view_one_data'))
    return render_template('home_page.html')

@app.route("/one")
def view_one_data():
    return render_template('view_one.html')

@app.route("/all")
def get_all_data():
    """get all data in bdd"""
    conn,cur = connect()

    cur.execute("SELECT * FROM data")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(data)

def add_data(name, value):
    try:
        conn,cur = connect()
        cur.execute(f"INSERT INTO data (name, value) VALUES ('{name}','{value}')")
        conn.commit()
        cur.close()
        conn.close()
        return {"status" : "success"}
    except Exception as e:
        return {"status" : "failed"}

def get_data(cur, id):
    cur.execute(f"SELECT * FROM data WHERE id={id}")
    data = cur.fetchone()
    print(json.dumps(data))
    return data

def update_data(cur, conn, id, name, value):
    try:
        cur.execute(f"UPDATE data SET name = '{name}', value = '{value}'  WHERE id = {id}")
        conn.commit()
        return {"status" : "success"}
    except Exception as e:
        return {"status" : "failed"}

def remove_data(cur, conn, id):
    try:
        cur.execute(f"DELETE FROM table WHERE id={id}")
        conn.commit()
        return {"status" : "success"}
    except Exception as e:
        return {"status" : "failed"}
    

if __name__=="__main__":
    app.run()
