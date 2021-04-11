from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__ENGINE = create_engine("sqlite:///../resources/data/db.sqlite", echo=True)
BASE = declarative_base()


def with_session(function: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        """
        Executes the specified function inside a SQLAlchemy session.
        :param args: The arguments to pass to the function.
        :param kwargs: The key-word arguments to pass to the function.
        :return: The result of the function.
        """
        session = sessionmaker(__ENGINE)()
        try:
            result = function(*args, **kwargs)
            session.commit()
            return result
        except Exception as exception:
            session.rollback()
            raise exception
        finally:
            session.close()

    return wrapper
