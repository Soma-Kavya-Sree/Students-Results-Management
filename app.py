from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = "students.json"

# Load student records
def load_records():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Save student records
def save_records(records):
    with open(DATA_FILE, "w") as file:
        json.dump(records, file, indent=4)

@app.route('/')
def index():
    records = load_records()
    return render_template('index.html', records=records)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        gpa = float(request.form['gpa'])
        department = request.form['department']

        records = load_records()
        if student_id in records:
            return "Student ID already exists!"
        
        records[student_id] = {
            "name": name,
            "gpa": gpa,
            "department": department
        }
        save_records(records)
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/update/<student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    records = load_records()
    if student_id not in records:
        return "Student not found!"
    
    if request.method == 'POST':
        records[student_id]['name'] = request.form['name']
        records[student_id]['gpa'] = float(request.form['gpa'])
        records[student_id]['department'] = request.form['department']
        save_records(records)
        return redirect(url_for('index'))
    return render_template('update_student.html', student=records[student_id], student_id=student_id)

@app.route('/delete/<student_id>')
def delete_student(student_id):
    records = load_records()
    if student_id in records:
        del records[student_id]
        save_records(records)
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search_student():
    records = load_records()
    if request.method == 'POST':
        student_id = request.form['student_id']
        if student_id in records:
            return render_template('search_student.html', student=records[student_id], found=True)
        else:
            return render_template('search_student.html', found=False)
    return render_template('search_student.html')

if __name__ == '__main__':
    app.run(debug=True)
