from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    is_completed = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()


def save_list_to_file():
    tasks = Todo.query.all()
    task_data = []
    for task in tasks:
        task_data.append({
            'task': task.task,
            'is_completed': task.is_completed,
            'date_added': task.date_added.strftime('%d-%m-%Y %H:%M:%S')
        })

    with open('todo_list.json', 'w') as file:
        json.dump(task_data, file, indent=4)


def load_list_from_file():
    if not os.path.exists('todo_list.json'):
        return

    with open('todo_list.json', 'r') as file:
        task_data = json.load(file)

    for item in task_data:
        task = Todo(
            task=item['task'],
            date_added=datetime.strptime(
                item['date_added'], '%d-%m-%Y %H:%M:%S'),
            is_completed=item['is_completed']
        )
        db.session.add(task)
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_name = request.form.get('content')
        if task_name:
            task = Todo(task=task_name)
            db.session.add(task)
            db.session.commit()
            flash('Task added.', 'success')
        else:
            flash('Type your task first.', 'error')
        return redirect('/')

    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:task_id>')
def remove_task(task_id):
    task = Todo.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted.', 'success')
    else:
        flash('Task not found', 'error')
    return redirect('/')


@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    task = Todo.query.get(task_id)
    if task:
        task.is_completed = True
        db.session.commit()
        flash('Task was completed', 'success')
    else:
        flash('Task not found', 'error')
    return redirect('/')


@app.route('/save/', methods=['GET', 'POST'])
def save_list():
    tasks = Todo.query.all()
    if tasks:
        save_list_to_file()
        flash('List was saved to todo_list.json.', 'success')
    else:
        flash('Cannot save list - add a task first.', 'error')
    return redirect('/')


@app.route('/load/', methods=['GET', 'POST'])
def load_list():
    load_list_from_file()
    flash('List loaded from todo_list.json', 'success')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
