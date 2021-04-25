# сессия для базы данных

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec


# абстрактная база
SqlAlchemyBase = dec.declarative_base()
# фабрика подключений
__factory = None


def global_init(db_file):
    # инициализация базы данных
    # делаем фабрику подключений глобально видимой
    global __factory
    # существует ли фабрика
    if __factory:
        return
    # проверка правильности указания пути к базе данных
    if not db_file or not db_file.strip():
        raise Exception('Необходимо указать файл базы данных.')
    # адрес подключения с параметрами для sqlachemy.
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f'Подключение к базе данных по адресу {conn_str}')
    engine = sa.create_engine(conn_str, echo=False)
    # создаем фабрику подключений и биндим её с движком
    __factory = orm.sessionmaker(bind=engine)
    # импорт списка моделей
    # с подавлением ошибки Unused import statement
    # noinspection PyUnresolvedReferences
    from . import __all_models
    # окончательно заставляем базу данных создать все ещё не созданные объекты
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    # создание сессии подключения к базе данных
    global __factory
    return __factory()
