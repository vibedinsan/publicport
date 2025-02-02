import os

# Define folder structure
folders = [
    "job_portal",
    "job_portal/templates",
    "job_portal/static"
]

files = {
    "job_portal/app.py": """from flask import Flask, render_template
from models import db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database created successfully!")
    app.run(debug=True)
""",
    "job_portal/models.py": """from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'))
""",
    "job_portal/forms.py": """from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    user_type = SelectField('User Type', choices=[('seeker', 'Job Seeker'), ('employer', 'Employer')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
""",
    "job_portal/templates/index.html": """<!DOCTYPE html>
<html>
<head>
    <title>Job Portal</title>
</head>
<body>
    <h1>Welcome to Job Portal</h1>
    <a href="{{ url_for('index') }}">Home</a>
</body>
</html>
""",
    "job_portal/static/style.css": """body {
    font-family: Arial, sans-serif;
    margin: 20px;
    padding: 20px;
}""",
    "job_portal/requirements.txt": """Flask
Flask-SQLAlchemy
Flask-Login
Flask-WTF
WTForms
Werkzeug"""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files and write content
for file_path, content in files.items():
    with open(file_path, "w") as file:
        file.write(content)

print("✅ Job portal folder structure created successfully!")
