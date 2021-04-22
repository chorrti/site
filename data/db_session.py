# сессия для базы данных

import sqlalchemy as sa
import sqlalchemy.orm as orm  # Модуль, отвечающий за функциональность ORM.
from sqlalchemy.orm import Session  # Класс, отвечающий за соединение с базой данных.
import sqlalchemy.ext.declarative as dec  # Модуль для объявления (декларации) базы данных.


# абстрактная база
SqlAlchemyBase = dec.declarative_base()
# фабрика подключений
__factory = None


def global_init(db_file):
    # инициализация базы данных

    # делаем фабрику подключений
    # глобально видимой:
    global __factory
    # Если фабрика уже создана и содержит какое-нибудь подключение, выходим из функции
    if __factory:
        return
    # проверка правильности указания пути к базе данных:
    if not db_file or not db_file.strip():
        raise Exception('Необходимо указать файл базы данных.')
    # адрес подключения с параметрами для SQLAlchemy.
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f'Подключение к базе данных по адресу {conn_str}')
    engine = sa.create_engine(conn_str, echo=False)
    # создаем фабрику подключений и биндим её с движком :
    __factory = orm.sessionmaker(bind=engine)

    # импорт списка моделей
    # с подавлением ошибки 'Unused import statement'
    # noinspection PyUnresolvedReferences
    from . import __all_models

    # окончательно заставляем базу данных создать все объекты,
    # которые она ещё не создала:
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    # создание сессии подключения к базе данных
    global __factory
    return __factory()
