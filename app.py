from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    college = db.Column(db.String(100))

    def __init__(self, name, college):
        self.name = name
        self.college = college

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        with app.app_context():
            name = request.form['name']
            college = request.form['college']
            student = Student(name=name, college=college)
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('success'))
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/view_data')
def view_data():
    with app.app_context():
        students = Student.query.all()
        return render_template('view_data.html', students=students)

@app.route('/clear_data', methods=['POST'])
def clear_data():
    with app.app_context():
        db.session.query(Student).delete()
        db.session.commit()
    return redirect(url_for('view_data'))

if __name__ == '__main__':
    if not os.path.exists('data.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
