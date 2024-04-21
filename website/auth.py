from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Staff,Students,Classes,Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get("username")
        password = request.form.get("password")
        user = Staff.query.filter_by(email=email).first()
        user_admin = Admin.query.filter_by(email=email).first()
        if user:
            if password == user.password:
                login_user(user,remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                error = 2
        elif user_admin:
            if password == user_admin.password:
                login_user(user_admin,remember=True)
                return redirect(url_for('auth.admin'))
            else:
                error = 2
        else:
            error = 1

        
    return render_template("login.html",error=0)
# error: 0 for no error, 1 for email does not exit , 2 for username and password does not match

@auth.route('admin',methods=['GET','POST'])
@login_required
def admin():
    staffs = Staff.query.all()
    return render_template("admin_staff.html",staffs=staffs,user=current_user)

@auth.route('admin/staff',methods=['GET','POST'])
@login_required
def adminStaff():
    staffs = Staff.query.all()
    if request.method == 'POST':
        query = request.form['query']
        staffs = Staff.query.filter(Staff.name.contains(query)).all()
    return render_template("admin_staff.html",staffs=staffs,user=current_user)

@auth.route('admin/student',methods=['GET','POST'])
@login_required
def adminStudent():
    students = Students.query.all()
    if request.method == 'POST':
        query = request.form['query']
        students = Students.query.filter(Students.name.contains(query)).all()
    return render_template("admin_student.html",students=students,user=current_user)

@auth.route('admin/classes',methods=['GET','POST'])
@login_required
def adminClasses():
    staffs = Classes.query.all()
    return render_template("admin_classes.html",staffs=staffs,user=current_user)

@auth.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))