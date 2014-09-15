import json

from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required

from main import application
from forms import *
from models import *
from utils import validated_password, hashed_password
from config import Configuration

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = '/signin/'

@login_manager.user_loader
def load_user(id):
    """ Query authenticated users and return. """
    return Users.query.get(id)


# need to separate views to views.py someday to manage things easily
@application.route('/')
def index():
    return render_template("index.html", page_title='Conversed / Your online presence!')

@application.route('/<username>/')
def userpage(username=None):
    user = Users.query.filter_by(username=username).first()
    if not user:
        user = Users()
        user.username = username
        user.firstname = u'Shaktimaan, is that you?'
        user.lastname = u''
        user.tagline = u'You are very special, you\'ll never be forgotten!'
        user.bio = u'Explain the rest of the world, why you are the most unique person to look at!'
        user.avatar = u'/static/Shaktimaan.jpg'
        return render_template('aboutme.html', page_title='Claim this name: '+username, user=user, projectsform=ProjectsForm())
    return render_template('aboutme.html', page_title=user.firstname+' '+user.lastname, user=user, projectsform=ProjectsForm())

@application.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = SignupForm(request.form)
        if form.validate():
            if form.password.data != form.repassword.data:
                form.repassword.errors.append(u'Passwords doesn\'t match.')
                return render_template('signup.html', signup_form=form, page_title='Signup to Conversed!')
            user = Users()
            user_exists = Users.query.filter_by(username=form.username.data).first()
            email_exists = Users.query.filter_by(email=form.email.data).first()
            if user_exists:
                form.username.errors.append(u'Username already taken')
            if email_exists:
                form.email.errors.append(u'Email already in use')
            if user_exists or email_exists:
                return render_template('signup.html', signup_form=form, page_title='Signup to Conversed!')
            else:
                # For testing purpose not created the form to take this data by users
                # need to fix
                # still populating data this way
                user.username = form.username.data
                user.email = form.email.data
                user.password = hashed_password(form.password.data.strip())
                user.firstname = u"foo"
                user.lastname = u"bar"
                user.tagline = u"foobar"
                user.bio = u"foobarfoobarfoobar foobarfoobar foobar foobar foobarfoobar foobarfoobarfoobar"
                user.avatar = '/static/favicon.png'
                db.session.add(user)
                db.session.commit()
                return render_template('signup_success.html', user=user, page_title='Registered to Conversed!')
        else:
            return render_template('signup.html', signup_form=form, page_title='Signup to Conversed!')
    return render_template('signup.html', signup_form=SignupForm(), page_title='Signup to Conversed!')

@application.route('/signin/', methods=['POST', 'GET'])
def signin():
    form = SigninForm(request.form)
    if request.method == 'POST':
        if current_user is not None and current_user.is_authenticated():
            return redirect(url_for('index'))
        if form.validate():
            user = Users.query.filter_by(username=form.username.data).first()
            if user is None:
                form.password.errors.append(u'Username or Password is wrong.')
                return render_template('signin.html', signin_form=form, page_title='Signin to Conversed!')
            # Make use of utils.safepass here
            if not validated_password(user.password, form.password.data):
                form.password.errors.append(u'Username or Password is wrong.')
                return render_template('signin.html', signin_form=form, page_title='Signin to Conversed!')
            login_user(user, remember=form.remember_me.data)
            session['signed'] = True
            session['username']= user.username
            if session.get('next'):
                next_page = session.get('next')
                session.pop('next')
                return redirect(next_page)
            else:
                return redirect(url_for("index"))
        else:
            return render_template('signin.html', signin_form=form, page_title='Signin to Conversed!')
    else:
        session['next'] = request.args.get('next')
        return render_template('signin.html', signin_form=SigninForm(), page_title='Signin to Conversed!')

# Not implemented yet
@application.route('/profile/', methods=['POST', 'GET'])
@login_required
def profile():
    return render_template('profile.html', page_title='Your online profile')

@application.route('/project_get/<id>')
def project_get(id):
    project = Portfolio.query.get(id)
    return json.dumps(project._asdict())

@application.route('/project_delete/<id>') 
def project_delete(id):
    project = Portfolio.query.get(id)
    db.session.delete(project)
    db.session.commit()
    result = {}
    result['result'] = 'success';
    return json.dumps(result)

@application.route('/project_update/', methods = ['POST'])
def project_update():
    form = ProjectsForm(request.form)
    if form.validate():
        result = {}
        result['iserror'] = False
        print form.project_id
        if not form.project_id.data:
            print 2
            user = Users.query.filter_by(username=session['username']).first()
            print session['username']
            if user is not None:
                user.portfolio.append(Portfolio(title=form.title.data, description=form.description.data, tags=form.tags.data))
                db.session.commit()
                result['savedsuccess'] = True 
            else:
                result['savedsuccess'] = False
        else:
            print 3
            project = Portfolio.query.get(form.project_id.data)
            print project
            form.populate_obj(project)
            db.session.commit()
            result['savedsuccess'] = True
            
        return json.dumps(result)
 
    form.errors['iserror'] = True
    return json.dumps(form.errors)

@application.route('/signout/', methods=['GET'])
def signout():
    try:
        session.pop('signed')
        username = session.pop('username')
        logout_user()
        return render_template('signout.html', page_title='Signned out succesfully!', username=username)
    except KeyError:
        return redirect(url_for('signin'))
