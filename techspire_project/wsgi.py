"""
WSGI config for techspire_project.
"""
import os
import shutil
from pathlib import Path
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techspire_project.settings')

# In Vercel serverless environment, copy the pre-seeded SQLite database to writable /tmp
if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
    base_dir = Path(__file__).resolve().parent.parent
    src_db = base_dir / 'db.sqlite3'
    dest_db = Path('/tmp/db.sqlite3')
    if src_db.exists() and not dest_db.exists():
        try:
            shutil.copy2(src_db, dest_db)
        except Exception as e:
            print(f"Notice: SQLite copy to /tmp: {e}")

application = get_wsgi_application()
app = application
