from contextlib import contextmanager
from typing import Callable, Iterable

from django.db import connections


@contextmanager
def switch_user(user: str):
    """
    In the scope of the context manager
    all queries are executed in the privileges of the given `user`.

    @param user: the name of the database user
    """
    for connection in connections.all():
        connection.execute_wrappers.append(_switch_user(user))
    try:
        yield
    finally:
        for connection in connections.all():
            with connection.cursor() as cursor:
                cursor.execute("SET SESSION AUTHORIZATION DEFAULT;")
            connection.execute_wrappers.pop()


def _switch_user(username) -> Callable:
    """
    Append a statement for switching user
    at the beginning of the SQL query.

    @param username: the name of the database user who will be the `current_user` for the executed queries
    @return: a callable which can be used as an execute wrapper for the connection
    """

    def wrapper(execute: Callable, sql: str, params: Iterable, many: bool, context: dict):
        new_sql = f"SET SESSION AUTHORIZATION {username};\n{sql}"
        return execute(new_sql, params, many, context)

    return wrapper

