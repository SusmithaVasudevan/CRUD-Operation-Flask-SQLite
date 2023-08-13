import json
import sqlite3
from flask import Flask, jsonify, Response, request

app = Flask(__name__)
PATH = "/Users/susmitha/PycharmProjects/FlaskTest/DatabaseFiles/database.db"


def connect_to_db():
    conn = sqlite3.connect(PATH, check_same_thread=False)
    return conn


def create_student_table():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute( "CREATE TABLE IF NOT EXISTS student (id INTEGER PRIMARY KEY ,name TEXT , rollno INTEGER UNIQUE NOT NULL ,dob DATE)")
        conn.commit()
    except:
        print("Student table creation failed")
    finally:
        conn.close()


@app.route('/student/<int:studentID>', methods=['GET'])
def get_student(studentID):
    conn = connect_to_db()
    cursor = conn.cursor()
    student_data = cursor.execute("SELECT * FROM student WHERE id = ?", (studentID,)).fetchone()

    if student_data is None:
        return jsonify({'Message': 'Student not found'}), 404

    # student_dict = {'id': student_data[0],'name': student_data[1],'rollno': student_data[2],'dob': student_data[3] }
    return Response(json.dumps(student_data), status=200)


@app.route('/student', methods=['POST'])
def student_create():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    id = data.get('id')
    name = data.get('name')
    rollno = data.get('rollno')
    dob = data.get('dob')
    if not all([id, rollno, name, dob]):
        return Response(json.dumps({'error': 'Incomplete student data'}), status=400)
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO student (id, name,rollno, dob) VALUES (?, ?, ?,?)", (id, name, rollno, dob))
        conn.commit()
        return jsonify({'message': 'Student created'}), 201
    except sqlite3.IntegrityError:
        return Response(json.dumps({'error': 'Duplicate id'}), status=409)
    finally:
        conn.close()

@app.route('/student/<int:student_id>', methods=['PUT'])
def student_update(student_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    rollno = data.get('rollno')
    name = data.get('name')
    dob = data.get('dob')
    if not all([id, rollno, name, dob]):
        return Response(json.dumps({'error': 'Incomplete student data'}), status=400)
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE student SET rollno=?, name=?, dob=? WHERE id=?', (rollno, name, dob, student_id))
        conn.commit()
        return jsonify({'message': 'Student updated', 'id': student_id}), 200
    except sqlite3.IntegrityError:
        return Response(json.dumps({'error': 'Duplicate id'}), status=409)


if __name__ == "__main__":
    create_student_table()
    app.run(debug=True)
