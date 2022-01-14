from django.db import connection

def db_username(user) -> str:
    with connection.cursor() as cursor: 
        cursor.execute("SELECT db_username(%s)", (user.pk,))
        return cursor.fetchone()[0]

