import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def init_sqlite_db():
    connection = sqlite3.connect("database.db")
    print("database connection successful")

    connection.execute("CREATE TABLE IF NOT EXISTS students(name TEXT, address TEXT, city TEXT, pin TEXT)")
    print("tables created successfully")

    connection.close()


init_sqlite_db()


@app.route(("/"))
@app.route('/enter-new/')
def enter_new_student():
    return render_template("student.html")


@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        try:
            name = request.form['name']
            address = request.form['address']
            city = request.form['city']
            pin = request.form['pin']

            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO students (name, address, city, pin) VALUES ('{name}', '{address}', '{city}', '{pin}')")
                connection.commit()
                msg = "Record successfully added."
                
        except Exception as e:
            connection.rollback()
            msg = f"Error occurred in insert operation: {e}"
        finally:
            connection.close()
            return render_template('result.html', msg=msg)


@app.route('/show-students-data')
def show_data():

    with sqlite3.connect('database.db') as connection:
        cur = connection.cursor()
        cur.execute("SELECT * FROM students")

        results = cur.fetchall()

    return jsonify(results)