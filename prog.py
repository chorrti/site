from flask import Flask, render_template, request, make_response, session, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from werkzeug.utils import redirect
from data import db_session
from data.users import User
from data.login import LoginForm
from data.register import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# инициализация менеджера логинов
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/index')
@app.route('/')
def index():
    # стартовая страница
    return render_template("homepage.html", user=current_user)


@login_manager.user_loader
def load_user(user_id):
    # загрузка пользователя
    db = db_session.create_session()
    return db.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # страница регистрации
    regform = RegisterForm()
    if regform.validate_on_submit():
        if regform.password.data != regform.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=regform,
                                   message='Пароли не совпадают')
        db = db_session.create_session()
        if db.query(User).filter(User.email == regform.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=regform,
                                   message='Такой пользователь уже есть')
        print(current_user)
        user = User(name=regform.name.data,
                    email=regform.email.data,
                    about=regform.about.data)
        user.set_password(regform.password.data)
        db.add(user)
        db.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=regform)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # авторизация пользователя
    form = LoginForm()
    if form.validate_on_submit():
        db = db_session.create_session()
        user = db.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    # выход из аккаунта
    logout_user()
    return redirect('/')


@app.route('/profile')
def profile():
    #image_file = url_for('static', filename='profile_pics/' + current_user.image)
    return render_template('profile.html', user=current_user)


if __name__ == '__main__':
    db_session.global_init('db/blogs.sqlite')
    app.run(host='127.0.0.1', port=8080)

# href="{{ url_for('static', filename='css/multiColumnTemplate.css') }}"

#<p>{{form.image(class="form-control")}}</p>