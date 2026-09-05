"""
WSGI config for techspire_project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techspire_project.settings')
application = get_wsgi_application()

if os.environ.get('VERCEL'):
    try:
        from django.core.management import call_command
        call_command('migrate', interactive=False)
        try:
            call_command('seed_techspire_data')
        except Exception as seed_err:
            print(f"Seeding notice: {seed_err}")
    except Exception as err:
        print(f"Migration error: {err}")

app = application


