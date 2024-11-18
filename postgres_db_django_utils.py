import os
from functools import wraps
import django


def manage_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Set up Django settings (adjust the path as needed)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postgres_db_django.settings')
        django.setup()

        # Execute the function
        func(*args, **kwargs)

    return wrapper