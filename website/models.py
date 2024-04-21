from . import db #import db object from current package
from flask_login import UserMixin
from sqlalchemy.sql import func

class Staff(db.Model,UserMixin):
    staff_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    classes = db.relationship('Classes')
    def get_id(self):
        return str(self.staff_id)

class Students(db.Model):
    student_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150))
    group = db.Column(db.Integer)
    def get_id(self):
        return str(self.student_id)

class Classes(db.Model):
    class_id = db.Column(db.Integer,primary_key=True)
    time = db.Column(db.DateTime)
    staff_id = db.Column(db.Integer,db.ForeignKey('staff.staff_id'))
    student_id = db.Column(db.Integer,db.ForeignKey('students.student_id'))
    attendance = db.Column(db.Integer) #0 for absent, 1 for present
    def get_id(self):
        return str(self.class_id)

class Admin(db.Model,UserMixin):
    admin_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    def get_id(self):
        return str(self.admin_id)
    
    

    
