from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt, generate_password_hash


from config import BaseConfig
from resources.reviews import review_api


import forms
import models


app = Flask(__name__)
app.register_blueprint(review_api)
app.secret_key = BaseConfig.SECRET_KEY #'generated_string'


#app.config.from_object('socialnetwork_app.config.DevelopmentConfig')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view ='login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """ connect to db before each request. """
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    g.db.close
    return response

@app.route('/register', methods=('GET', 'POST'))
def register():
    form=forms.RegistrationForm()
    if form.validate_on_submit():
        flash("You registered",'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
            )
        return redirect(url_for('index'))
    return render_template('register.html',form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Wrong credentials","error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in !","success")
                return redirect(url_for('index'))
            else:
                flash("Wrong credentials","error")
    return render_template('login.html', form=form)


@app.route('/new_post', methods=('GET', 'POST'))
@login_required
def post():
    form=forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(user=g.user._get_current_object(),
            content= form.content.data.strip()
            )
        flash('Message posted', 'success')
        return redirect(url_for('index'))
    return render_template('post.html',form=form)


@app.route('/')
def index():
    stream = models.Post.select().limit(100)
    return render_template('stream.html', stream=stream)

@app.route('/stream')
@app.route('/stream/<username>')
@login_required
def stream(username=None):
    template="stream.html"
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            stream = user.posts.limit(100)
    else:
        stream = current_user.get_stream().limit(100)
        user = current_user
    if username:
        template = 'user_stream.html'
    return render_template(template, stream=stream, user=user)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    posts = models.Post.select().where(models.Post.id == post_id)
    if posts.count() == 0:
        abort(404)
    return render_template('stream.html',stream=posts)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logout", "success")
    return redirect(url_for('index'))

@app.route('/follow/<username>')
@login_required
def follow(username):
    try:
        to_user = models.User.get(models.User.username**username)

    except models.DoesNotExist:
        abort(404)

    else:
        try:
            models.Relationship.create(
                from_user = g.user._get_current_object(),
                to_user=to_user
                )
        except models.IntegrityError:
            pass
        else:
            flash(f"You're a now following {to_user.username}",'success')

    return redirect(url_for('stream', username=to_user.username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    try:
        to_user = models.User.get(models.User.username**username)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Relationship.get(
                from_user = g.user._get_current_object(),
                to_user=to_user
                ).delete_instance()
        except models.IntegrityError:
            pass
        else:
            flash(f"You're unfollowed {to_user.username}",'success')

    return redirect(url_for('stream', username=to_user.username))

@app.route('/change_password/<username>', methods=('GET', 'POST'))
@login_required
def change_password(username):
    form=forms.ChangePasswordForm()
    if form.validate_on_submit():
        models.User.update(password=generate_password_hash(form.password_to_change.data)).where(
            models.User.username == username).execute() 
        flash('Password has been updated!', 'success')
        return redirect(url_for('index'))
    return render_template('profile.html', form=form)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__== '__main__':
    models.initialize()
    try:
        models.User.create_user(username='Denis',
                                email='frunzadenis.93@gmail.com',
                                password='pass',
                                admin=True
                                )
    except ValueError:
        pass
    app.run(debug=BaseConfig.DEBUG, port=BaseConfig.PORT, host=BaseConfig.HOST)

