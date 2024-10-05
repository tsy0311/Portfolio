from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Project, BlogPost, Contact
from .forms import LoginForm, RegistrationForm, ProjectForm, BlogPostForm, ContactForm

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
admin = Blueprint('admin', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/projects')
def projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('projects.html', projects=projects)

@main.route('/blog')
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(new_contact)
        db.session.commit()
        flash('Your message has been sent!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=form)

@main.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@admin.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.all()
    posts = BlogPost.query.all()
    return render_template('admin/dashboard.html', projects=projects, posts=posts)

@admin.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        new_project = Project(title=form.title.data, description=form.description.data,
                              image_url=form.image_url.data, github_url=form.github_url.data,
                              live_url=form.live_url.data)
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_project.html', form=form)

@admin.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        new_post = BlogPost(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Blog post added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_post.html', form=form)