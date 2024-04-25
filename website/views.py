from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import login_required, logout_user, current_user
import os
from website import UPLOAD_FOLDER, multi
from werkzeug.utils import secure_filename
from .models import Students, Classes, Staff
from datetime import datetime
from sqlalchemy import and_
from . import db,camera
import cv2

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html",user=current_user)

# SINGLE FILE UPLOAD
# @views.route('test',methods=['GET','POST'])
# def test():
#     if request.method == 'POST':
#         if 'imageFile' not in request.files:
#             return redirect(url_for('views.test'))
        
#         file = request.files['imageFile']

#         if file.filename == '':
#             return redirect(url_for('views.test'))
        
#         if file:
#             filename = file.filename
#             file.save(os.path.join(UPLOAD_FOLDER, filename))
#             print("File saved as:", filename)
#             return redirect(url_for('views.test'))
#     return render_template("test.html")



# MULTIPLE FILE UPLOAD
@views.route('test',methods=['GET','POST'])
def test():
    record = []
    if request.method == 'POST':
        files = request.files.getlist('imageFiles')  # Retrieve multiple files
        for file in files:
            if file.filename == '':
                continue  # Skip if no file selected
            
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # print("File saved as:", filename)
        # facial recognition here
        multi.initialize_FR()
        data = multi.find_target_face_without_display()
        # multi.find_target_face()
        # multi.render_image()
        record.append(data)
    return render_template("test.html",records=record)




@views.route('dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    today_date = datetime.now()
    today_date_formatted = today_date.strftime("%Y-%m-%d")
    staff = current_user
    staff_classes = Classes.query.filter(and_(Classes.staff_id == staff.staff_id,Classes.end_time>today_date)).all()
    return render_template("dashboard.html",user=current_user,staff_classes=staff_classes,today_date=today_date_formatted)


@views.route('trial',methods=['GET','POST'])
def trial():
    return render_template("trial.html",user=current_user)

@views.route('dashboard/attendance/<int:classId>/<int:groupNum>',methods=['GET','POST'])
@login_required
def attendance(classId,groupNum):
    students = Students.query.filter(Students.group.contains(groupNum)).all()
    attendance = Classes.query.filter(Classes.class_id == classId).first().attendance
    length_of_students = len(students)
    if request.method == 'POST':
        query = request.form['query']
        students = Students.query.filter(Students.name.contains(query)).all()
    return render_template("attendance.html",user=current_user,students=students,classID=classId,attendance=attendance,length_of_students=length_of_students)

@views.route("admin/staff/add_new",methods=['GET','POST'])
@login_required
def add_staff():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        group = request.form['group']
        new_staff = Staff(name=name,email=email,password=password,group=group)
        db.session.add(new_staff)
        db.session.commit()
        return redirect(url_for('views.admin'))
    return render_template("admin_staff_addnew.html",user=current_user)

@views.route("admin/student/add_new",methods=['GET','POST'])
@login_required
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        group = request.form['group']
        new_student = Students(name=name,group=group)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('views.adminStudent'))
    return render_template("admin_student_addnew.html",user=current_user)

@views.route("admin/classes/add_new",methods=['GET','POST'])
@login_required
def add_classes():
    if request.method == 'POST':
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        staff_id = request.form['staff_id']
        group = request.form['group']
        new_class = Classes(start_time=start_time,end_time=end_time,staff_id=staff_id,group=group,attendance="0")
        db.session.add(new_class)
        db.session.commit()
        return redirect(url_for('views.adminClasses'))
    return render_template("admin_classes_addnew.html",user=current_user)

@views.route("dashboard/take_attendance/<int:classId>",methods=['GET','POST'])
@login_required
def take_attendance(classId):
    return render_template("take_attendance.html",user=current_user)

@views.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')