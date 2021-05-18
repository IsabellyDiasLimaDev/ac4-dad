from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db
from app.model.tables import *

@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['nome']
        email = request.form['login']
        password = request.form['senha']

        user = User(name, email, password,0,0)
        db.session.add(user)
        db.session.commit()
        return render_template('login.html')
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not User or not user.verify_password(password):
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile/<username>', methods=['GET'])
def profile(username):
    user = User.query.filter_by(email=username).first()
    return render_template('edit_user.html', user=user)

@app.route('/profilepost/<id_user>', methods=['GET'])
def profile_post(id_user):
    user = User.query.filter_by(id=id_user).first()
    return render_template('edit_user.html', user=user)

@app.route('/changepassword/<user>', methods=['POST'])
def change_password(user):
    password = request.form['password']
    user = User.query.filter_by(email=user).first()
    user.set_password(password)
    db.session.commit()
    return redirect(url_for('profile',username=user.email))

@app.route('/changeuser/<email>', methods=['POST'])
def change_user(email):
    email_change = request.form['user']
    user = User.query.filter_by(email=email).first()
    user.email = email_change
    db.session.commit()
    return redirect(url_for('profile', username=user.email))

@app.route('/follow/<id_user>/<follower>', methods=['GET'])
def follow(id_user,follower):
    current_user = User.query.filter_by(email=follower).first()
    following = User.query.filter_by(id=id_user).first()

    follow = Follow(following.id,current_user.id)

    current_user.following += 1
    following.followers += 1

    db.session.add(follow)
    db.session.commit()
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/posting/<username>", methods=['POST'])
def posting(username):
    user = User.query.filter_by(email=username).first()
    conteudoPost = request.form['postConteudo']

    posting = Post(conteudoPost, user.id)
    db.session.add(posting)
    db.session.commit()
    posts = Post.query.all()
    return render_template('home.html', posts=posts)
