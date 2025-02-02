import os
from flask import Flask, render_template, redirect, url_for, request, flash,url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'seeker' or 'employer'

# Job Model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    jobs = Job.query.all()
    return render_template('index.html', jobs=jobs)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = generate_password_hash(request.form['password'])
#         user_type = request.form['user_type']
#         user = User(email=email, password=password, user_type=user_type)
#         db.session.add(user)
#         db.session.commit()
#         flash('Registration successful! Please login.', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        user_type = request.form['user_type']
        user = User(email=email, password=password, user_type=user_type)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials, try again.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 'employer':
        jobs = Job.query.filter_by(posted_by=current_user.id).all()
    else:
        jobs = Job.query.all()
    return render_template('dashboard.html', jobs=jobs)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    if request.method == 'POST' and current_user.user_type == 'employer':
        title = request.form['title']
        description = request.form['description']
        company = request.form['company']
        job = Job(title=title, description=description, company=company, posted_by=current_user.id)
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('post_job.html')


@app.route('/apply')
def apply():
    return render_template('apply.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database created successfully!")     
    #port = int(os.environ.get("PORT", 5000))  # Use Render's dynamic port
    app.run(host="0.0.0.0", port=5000)

    
    