from flask import Flask, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect, secure_filename
from data import db_session
from data.users import User
from data.login import LoginForm
from data.builds import BuildForm, Builds
from data.news import NewsForm, News
from data.teams import TeamForm, Teams
from data.register import RegisterForm

app = Flask(__name__)
# защита приложения ключом
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# инициализация менеджера логинов
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/homepage')
@app.route('/')
def homepage():
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
        # проверка на уже существующего пользователя/несовпадение паролей/имени пользователя
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
        if db.query(User).filter(User.name == regform.name.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=regform,
                                   message='Пользователь с таким именем уже есть')
        # вытаскиваем и сохраняем картинку, загруженную пользователем
        # f = regform.pic.data
        # filename = secure_filename(f.filename)
        # print(url_for('static', filename='profile_pics/' + '123.png'))
        # f.save(url_for('static', filename='profile_pics/' + '123.png'))
        # сохраняем юзера в базу
        user = User(name=regform.name.data,
                    email=regform.email.data,
                    about=regform.about.data)
        user.set_password(regform.password.data)
        db.add(user)
        db.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=regform, user=current_user)


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
    return render_template('login.html', title='Авторизация', form=form, user=current_user)


@app.route('/logout')
@login_required
def logout():
    # выход из аккаунта
    logout_user()
    return redirect('/homepage')


@app.route('/profile')
def profile():
    # страница профиля
    # image_file = url_for('static', filename='profile_pics/' + current_user.pic)
    return render_template('profile.html', user=current_user)


@app.route('/index')
def index():
    # лента сообщений
    db = db_session.create_session()
    news = db.query(News)
    return render_template("index.html", news=news, user=current_user,  title='Лента')


@app.route('/index_builds')
def index_builds():
    # лента билдов
    db = db_session.create_session()
    builds = db.query(Builds)
    return render_template("index_builds.html", builds=builds, user=current_user, title='Билды')


@app.route('/index_teams')
def index_teams():
    # лента команд
    db = db_session.create_session()
    teams = db.query(Teams)
    return render_template("index_teams.html", teams=teams, user=current_user, title='Команды')


@app.route('/post', methods=['GET', 'POST'])
@login_required
def simple_post():
    # создание обычного поста
    form = NewsForm()
    if form.validate_on_submit():
        # заполняем таблицу значениями
        db = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        current_user.news.append(news)
        db.merge(current_user)
        db.commit()
        return redirect('/index')
    return render_template('news.html', title='Добавление новости', form=form, user=current_user)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    # удаление записи
    db = db_session.create_session()
    news = db.query(News).filter(News.id == id, News.user == current_user).first()
    if news:
        db.delete(news)
        db.commit()
    else:
        abort(404)
    return redirect('/index')


@app.route('/build_post', methods=['GET', 'POST'])
@login_required
def build_post():
    # создание обычного поста
    form = BuildForm()
    if form.validate_on_submit():
        # заполняем таблицу значениями
        db = db_session.create_session()
        build = Builds()
        build.character = form.character.data
        build.character_class = form.character_class.data
        build.artefacts = form.artefacts.data
        build.talents = form.talents.data
        build.content = form.content.data
        current_user.build_posts.append(build)
        db.merge(current_user)
        db.commit()
        return redirect('/index_builds')
    return render_template('build.html', title='Добавление билда', user=current_user, form=form)


@app.route('/builds_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def builds_delete(id):
    # удаление записи
    db = db_session.create_session()
    builds = db.query(Builds).filter(Builds.id == id, Builds.user == current_user).first()
    if builds:
        db.delete(builds)
        db.commit()
    else:
        abort(404)
    return redirect('/index_builds')


@app.route('/team_post', methods=['GET', 'POST'])
@login_required
def team_post():
    # создание поста с командой
    form = TeamForm()
    if form.validate_on_submit():
        # заполняем таблицу значениями
        db = db_session.create_session()
        team = Teams()
        team.character_1 = form.character_1.data
        team.character_2 = form.character_2.data
        team.character_3 = form.character_3.data
        team.character_4 = form.character_4.data
        team.character_class_1 = form.character_class_1.data
        team.character_class_2 = form.character_class_2.data
        team.character_class_3 = form.character_class_3.data
        team.character_class_4 = form.character_class_4.data
        team.artefacts = form.artefacts.data
        team.talents = form.talents.data
        team.content = form.content.data
        current_user.team_posts.append(team)
        db.merge(current_user)
        db.commit()
        return redirect('/index_teams')
    return render_template('team.html', title='Добавление команды', user=current_user, form=form)


@app.route('/teams_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def teams_delete(id):
    # удаление команды
    db = db_session.create_session()
    teams = db.query(Teams).filter(Teams.id == id, Teams.user == current_user).first()
    if teams:
        db.delete(teams)
        db.commit()
    else:
        abort(404)
    return redirect('/index_teams')


if __name__ == '__main__':
    db_session.global_init('db/blogs.sqlite')
    app.run(host='127.0.0.1', port=8080)

# href="{{ url_for('static', filename='css/multiColumnTemplate.css') }}"

# <p>{{form.image(class="form-control")}}</p>

# (в register html <p>
#			{{form.pic.label}}<br>
#			{{form.pic}}<br>
#		</p>)
