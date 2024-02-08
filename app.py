from flask import Flask, request, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import UserForm, UserLoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app=Flask(__name__)
app.config['SECRET_KEY']='key'
debug=DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO'] = True

def initialize():
    '''initializes the connection to database'''
    with app.app_context():
        connect_db(app)

initialize()

@app.route('/')
def base():
    '''redirects to "/register"'''
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    '''renders form to add new user'''
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username already exists')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        return redirect(f'/users/{username}')

    return render_template('register.html', form=form)

@app.route('/users/<username>')
def show_user_page(username):
    '''returns user page if user logged in, otherwise redirect to register'''
    if "username" not in session:
        return redirect('/register')
    user = User.query.get_or_404(username)
    user_feedback = user.feedback
    return render_template('user-page.html', user=user, feedback = user_feedback)

@app.route('/login', methods=['GET', 'POST'])
def show_and_handle_login():
    '''renders login form and handles form submission'''
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Invalid username/password.']
    return render_template('login.html', form=form)

@app.route('/logout')
def handle_logout():
    '''logs out user'''
    if session.get('username', None):

        session.pop('username')
    return redirect('/')

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    '''deletes user if user is logged in'''
    if username and username == session.get('username', None):
        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        return redirect('/')
    return redirect('/')
    
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def show_and_handle_feedback_form(username):
    '''renders and handles feedback form submission'''
    if username and username == session.get('username', None):
        form = FeedbackForm()
        user = User.query.get(username)
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            fb = Feedback(title = title, content = content, username = user.username)
            db.session.add(fb)
            db.session.commit()
            return redirect(f'/users/{username}')
        return render_template('feedback.html', form=form)
    return redirect('/')
    
@app.route('/feedback/<int:fbid>/update', methods=['GET', 'POST'])
def update_feedback(fbid):
    '''updates feedback'''
    fb = Feedback.query.get_or_404(fbid)
    if fb.username == session.get('username', None):
        form = FeedbackForm(obj=fb)
        if form.validate_on_submit():
            fb.title = form.title.data
            fb.content = form.content.data
            db.session.commit()
            return redirect(f'/users/{fb.username}')
        return render_template('feedback.html', form=form)
    return redirect('/')

@app.route('/feedback/<int:fbid>/delete', methods=["POST"])
def delete_feedback(fbid):
    '''deletes feedback'''
    fb = Feedback.query.get_or_404(fbid)
    username = fb.username
    if username == session.get('username', None):
        db.session.delete(fb)
        db.session.commit()
        return redirect(f'/users/{username}')
    return redirect('/')