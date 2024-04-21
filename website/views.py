from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, logout_user, current_user
import os
from website import UPLOAD_FOLDER, multi
from werkzeug.utils import secure_filename
from .models import Students


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
    return render_template("dashboard.html",user=current_user)


@views.route('trial',methods=['GET','POST'])
def trial():
    return render_template("trial.html",user=current_user)

@views.route('dashboard/attendance',methods=['GET','POST'])
def attendance():
    students = Students.query.filter(Students.group.contains(1)).all()
    if request.method == 'POST':
        query = request.form['query']
        students = Students.query.filter(Students.name.contains(query)).all()
    return render_template("attendance.html",user=current_user,students=students)
