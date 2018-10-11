#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mall.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)


# Traceback (most recent call last):

#   File "manage.py", line 22, in <module>
#     execute_from_command_line(sys.argv)

#   File "/home/python/.virtualenvs/django/lib/python3.6/site-packages/django/core/management/__init__.py", line 364, in execute_from_command_line
#     utility.execute()

#   File "/home/python/.virtualenvs/django/lib/python3.6/site-packages/django/core/management/__init__.py", line 338, in execute
#     django.setup()

#   File "/home/python/.virtualenvs/django/lib/python3.6/site-packages/django/__init__.py", line 27, in setup
#     apps.populate(settings.INSTALLED_APPS)

#   File "/home/python/.virtualenvs/django/lib/python3.6/site-packages/django/apps/registry.py", line 89, in populate
#     "duplicates: %s" % app_config.label)

# django.core.exceptions.ImproperlyConfigured: Application labels aren't unique, duplicates: rest_framework
