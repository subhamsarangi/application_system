from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(50))  # 'student' or 'admin'
    profile = db.relationship("StudentProfile", backref="user", uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    academic_background = db.Column(db.Text, nullable=False)
    gpa = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    application = db.relationship("Application", backref="profile", uselist=False)


class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(
        db.String(50), default="Submitted"
    )  # Submitted, Under Review, Approved, Rejected
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    decision_date = db.Column(db.DateTime)
    profile_id = db.Column(db.Integer, db.ForeignKey("student_profiles.id"))
    documents = db.relationship("Document", backref="application", lazy=True)


class Document(db.Model):
    __tablename__ = "documents"
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(50))
    file_name = db.Column(db.String(150))
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"))
