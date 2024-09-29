from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import User, Task, Achievement
from forms import LoginForm, TaskForm, AchievementForm, RegisterForm
from hashlib import sha256
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.hashed_password == sha256(form.password.data.encode('utf-8')).hexdigest():
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        flash('You have been logged in!', 'success')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, hashed_password=sha256(form.password.data.encode('utf-8')).hexdigest())
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/tasks')
@login_required
def tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if request.method == 'POST' and form.validate_on_submit():
        task = Task(title=form.title.data, description=form.description.data, date=form.date.data, done=form.done.data, user_id=current_user.id, priority=form.priority.data)
        db.session.add(task)
        db.session.commit()
        flash('Task added!', 'success')
        return redirect(url_for('tasks'))
    return render_template('add_task.html', form=form)

@app.route('/achievements')
@login_required
def achievements():
    achievements = Achievement.query.all()
    return render_template('achievements.html', achievements=achievements)

@app.route('/achievements/add', methods=['GET', 'POST'])
@login_required
def add_achievement():
    form = AchievementForm()
    if request.method == 'POST' and form.validate_on_submit():
        achievement = Achievement(title=form.title.data, description=form.description.data, date=form.date.data, user_id=current_user.id, priority=form.priority.data)
        db.session.add(achievement)
        db.session.commit()
        flash('Achievement added!', 'success')
        return redirect(url_for('achievements'))
    return render_template('add_achievement.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'success')
    return redirect(url_for('home'))

@app.route('/task/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!', 'success')
    return redirect(url_for('tasks'))

@app.route('/achievement/delete/<int:achievement_id>')
def delete_achievement(achievement_id):
    achievement = Achievement.query.get(achievement_id)
    db.session.delete(achievement)
    db.session.commit()
    flash('Achievement deleted!', 'success')
    return redirect(url_for('achievements'))

@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    form = TaskForm()
    if request.method == 'POST' and form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.date = form.date.data
        task.done = form.done.data
        task.priority = form.priority.data
        db.session.commit()
        flash('Task updated!', 'success')
        return redirect(url_for('tasks'))
    return render_template('edit_task.html', form=form, task=task)

@app.route('/achievement/edit/<int:achievement_id>', methods=['GET', 'POST'])
def edit_achievement(achievement_id):
    achievement = Achievement.query.get(achievement_id)
    form = AchievementForm()
    if request.method == 'POST' and form.validate_on_submit():
        achievement.title = form.title.data
        achievement.description = form.description.data
        achievement.date = form.date.data
        achievement.priority = form.priority.data
        db.session.commit()
        flash('Achievement updated!', 'success')
        return redirect(url_for('achievements'))
    return render_template('edit_achievement.html', form=form, achievement=achievement)
